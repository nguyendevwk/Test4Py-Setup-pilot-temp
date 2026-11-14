"""Count known upstream initialization steps without guessing LLM call totals."""
import inspect
from pilot.progress import emit

INITIALIZATION_STEPS = (
    'analyze_function_members', 'complete_file_imports', 'parseExtend',
    'parse_full_members', 'parseCG', 'analyze_functions', 'get_total_what_todo',
    'generate_summary', 'analyze_each_class', 'embedding_class_summary',
)


def instrument_initialization(project, work):
    names = [name for name in INITIALIZATION_STEPS if callable(getattr(project, name, None))]
    done = set()
    def start(name):
        emit(work, 'initialization', 'step_start', analysis_step=name,
             analysis_steps_completed=len(done), analysis_steps_total=len(names))
    def finish(name):
        done.add(name)
        emit(work, 'initialization', 'step_end', analysis_step=name,
             analysis_steps_completed=len(done), analysis_steps_total=len(names))
    def wrap(name, original):
        if inspect.iscoroutinefunction(original):
            async def tracked(*args, **kwargs):
                start(name)
                result = await original(*args, **kwargs)
                finish(name)
                return result
        else:
            def tracked(*args, **kwargs):
                start(name)
                result = original(*args, **kwargs)
                finish(name)
                return result
        return tracked
    for name in names:
        setattr(project, name, wrap(name, getattr(project, name)))
    emit(work, 'initialization', 'instrumented', analysis_steps_completed=0,
         analysis_steps_total=len(names), analysis_step='call graph / discovery before tracked steps')
