# Rendre

A Git-based CMS for parsing and emitting ATOM feeds.

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

### `gallery`

## Examples

