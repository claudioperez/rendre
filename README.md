---
title: Rendre
...

<h1>Rendre</h1>

A Git-based CMS for parsing and emitting ATOM feeds.

-----------------------------------------------------

[![PyPI Version][pypi-v-image]][pypi-v-link]
[![Commits since latest release][gh-image]][gh-link]

## Options

<dl>
<dt>-v/--verbose</dt>
<dd>Generate verbose console logging</dd>
<dt>-q/--quiet</dt>
<dd>Suppress all console logging</dd>
<dt>-i/--include-item &lt;item-selector&gt;</dt>
<dd>Include items that validate against <code>&lt;item-selector&gt;::=&lt;pointer&gt;&lt;separator&gt;&lt;pattern&gt;</code>. </dd>
</dl>

### \<pattern>

Patterns are currently handled as globs, supporting both `*` and `?` expansion.

### \<pointer>

Pointers which begin with a `/` character are treated as JSON pointers.

The following shorthand pointers are defined for `%`-prefixed pointers:

```
%i -> item['id']
%t -> /id | item['id']
%c -> /categories | item['categories']
```

### \<item-selector>

An item selector is a combination of a pointer and a pattern, separated by either `=` or `:`. 

If no unescaped separator is present, the pointer is implicitly taken as `%i`, and the full string is processed as the pattern.



## Commands

### `list`

### `filtered-gallery`

## Examples

```
>rendre list -i "%./api/cmd/usage:"

```


```
> rendre list -- %i %t %c/workflow-module %./links/repository[24:] | column -t -s ,
...
bknd-0035   ExtractPGA              performSIMULATION        SimCenter/SimCenterBackendApplications
bknd-0036   Dakota-FEM              performUQ                SimCenter/SimCenterBackendApplications
bknd-0037   Dakota-UQ               performUQ                SimCenter/SimCenterBackendApplications
bknd-0038   Dakota-UQ1              performUQ                SimCenter/SimCenterBackendApplications
bknd-0039   Dakota-UQ               performUQ                SimCenter/quoFEM
bknd-0040   DakotaFEM               performUQ                SimCenter/quoFEM
bknd-0041   SimCenterUQ-UQ          performUQ                SimCenter/quoFEM
bknd-0042   Other-UQ                performUQ                SimCenter/quoFEM
bknd-0043   UCSD-UQ                 performUQ                SimCenter/quoFEM
bknd-0044   pelicun                 performDL                SimCenter/SimCenterBackendApplications
bknd-0045   NearestNeighborEvents   performRegionalMapping   SimCenter/SimCenterBackendApplications
bknd-0046   OpenSees                performSIM               SimCenter/quoFEM
bknd-0047   OpenSeesPy              performSIM               SimCenter/quoFEM
...
```

## Sphinx Directive

```rst
.. rendre:: <command>
   :<cli-options>:

   :<cmd-options>:
```

[pypi-v-image]: https://img.shields.io/pypi/v/rendre.svg
[pypi-v-link]: https://pypi.org/project/rendre/

[gh-link]: https://github.com/claudioperez/rendre/compare/0.0.1...master
[gh-image]: https://img.shields.io/github/commits-since/claudioperez/rendre/0.0.1?style=social
