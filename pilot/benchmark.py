"""Frozen NA subset selection and module-level audit; no PyCG-specific setup claims."""
import math
import random
from pathlib import Path


def select_modules(projects, registry, count=19, seed=42):
    frame=sorted((p,m) for p in registry for m in projects[p])
    if not 1<=count<=len(frame):raise ValueError('count outside NA sampling frame')
    # Balanced project coverage before allocating the remaining modules.
    rng=random.Random(seed);groups={p:list(projects[p]) for p in sorted(registry)}
    for modules in groups.values():rng.shuffle(modules)
    selected=[]
    while len(selected)<count:
        for project in sorted(groups):
            if groups[project] and len(selected)<count:selected.append((project,groups[project].pop()))
    return [dict(project=p,module=m) for p,m in sorted(selected)]


def locate_module(root, module):
    relative=Path(*module.split('.'))
    candidates=[root/relative.with_suffix('.py'),root/'src'/relative.with_suffix('.py'),
                root/relative/'__init__.py',root/'src'/relative/'__init__.py']
    found=[p for p in candidates if p.is_file()]
    if len(found)!=1:raise ValueError(f'Expected one module source for {module}, found {found}')
    path=found[0];relative=path.relative_to(root)
    import_root=root/'src' if relative.parts[0]=='src' and module.split('.')[0]!='src' else root
    package=import_root/module.split('.')[0]
    return path,import_root,package.relative_to(root)


def module_coverage(coverage, relative):
    files=coverage.get('files',{})
    relative=relative.as_posix()
    matching=[v for k,v in files.items() if k.replace('\\','/')==relative or k.replace('\\','/').endswith('/'+relative)]
    if len(matching)!=1:return dict(line_pct=None,branch_pct=None,coverage_available=False)
    summary=matching[0].get('summary',{})
    def pct(a,b):return 100*a/b if a is not None and b else None
    return dict(line_pct=pct(summary.get('covered_lines'),summary.get('num_statements')),
        branch_pct=pct(summary.get('covered_branches'),summary.get('num_branches')),
        covered_lines=summary.get('covered_lines'),total_lines=summary.get('num_statements'),
        covered_branches=summary.get('covered_branches'),total_branches=summary.get('num_branches'),
        coverage_available=True)
