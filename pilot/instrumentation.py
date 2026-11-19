"""Count known upstream initialization steps without guessing LLM call totals."""
import inspect
from contextlib import contextmanager
from pilot.progress import emit

INITIALIZATION_STEPS = (
    'analyze_function_members', 'complete_file_imports', 'parseExtend',
    'parse_full_members', 'parseCG', 'analyze_functions', 'get_total_what_todo',
    'generate_summary', 'analyze_each_class', 'embedding_class_summary',
)


def instrument_initialization(project, work, function_database=None):
    names = [name for name in INITIALIZATION_STEPS if callable(getattr(project, name, None))]
    project_names=list(names)
    if function_database is not None:names.append('function_database_index')
    done = set()
    def start(name):
        emit(work, 'initialization', 'step_start', analysis_step=name,
             analysis_units_completed=0,analysis_units_total=None,
             analysis_steps_completed=len(done), analysis_steps_total=len(names))
    def finish(name):
        done.add(name)
        emit(work, 'initialization', 'step_end', analysis_step=name,
             analysis_steps_completed=len(done), analysis_steps_total=len(names))
    def wrap(name, original):
        @contextmanager
        def counted_items():
            namespace=getattr(getattr(original,'__func__',original),'__globals__',{})
            factory=namespace.get('tqdm')
            embedder=namespace.get('embedder')
            class Bar:
                def __init__(self,bar):
                    self.bar=bar
                    self.completed=getattr(bar,'n',0)
                    emit(work,'initialization','items',analysis_step=name,
                         analysis_units_completed=getattr(bar,'n',0),analysis_units_total=getattr(bar,'total',None))
                def __enter__(self):self.bar.__enter__();return self
                def __exit__(self,*args):return self.bar.__exit__(*args)
                def __getattr__(self,key):return getattr(self.bar,key)
                def update(self,n=1):
                    value=self.bar.update(n)
                    self.completed+=n
                    emit(work,'initialization','items',analysis_step=name,
                         analysis_units_completed=self.completed,analysis_units_total=self.bar.total)
                    return value
            if factory is not None:namespace['tqdm']=lambda *a,**kw:Bar(factory(*a,**kw))
            count_embeddings=embedder is not None and name in ('embedding_class_summary','function_database_index')
            if count_embeddings:
                if name=='embedding_class_summary':total=sum(len(f.classes) for f in project.file_messages)
                else:total=sum(fn.summary is not None for f in project.file_messages for fn in f.functions)
                class Embeddings:
                    completed=0
                    def __getattr__(self,key):return getattr(embedder,key)
                    def embed_query(self,*a,**kw):
                        value=embedder.embed_query(*a,**kw);self.completed+=1
                        emit(work,'initialization','items',analysis_step=name,
                             analysis_units_completed=self.completed,analysis_units_total=total)
                        return value
                namespace['embedder']=Embeddings()
                emit(work,'initialization','items',analysis_step=name,analysis_units_completed=0,analysis_units_total=total)
            try:yield
            finally:
                if factory is not None:namespace['tqdm']=factory
                if count_embeddings:namespace['embedder']=embedder
        if inspect.iscoroutinefunction(original):
            async def tracked(*args, **kwargs):
                start(name)
                with counted_items():result = await original(*args, **kwargs)
                finish(name)
                return result
        else:
            def tracked(*args, **kwargs):
                start(name)
                with counted_items():result = original(*args, **kwargs)
                finish(name)
                return result
        return tracked
    for name in project_names:
        setattr(project, name, wrap(name, getattr(project, name)))
    if function_database is not None:
        function_database.init=wrap('function_database_index',function_database.init)
    emit(work, 'initialization', 'instrumented', analysis_steps_completed=0,
         analysis_steps_total=len(names), analysis_step='call graph / discovery before tracked steps')
