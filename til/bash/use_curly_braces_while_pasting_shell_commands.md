# Use Curly Braces While Pasting Shell Commands

Pasting shell commands can be a pain when the command includes hidden return `\n` characters. In such a case, your shell will try to execute the command immediately. To prevent that, use curly braces `{ <cmd> }` while pasting the command. Your command
should look like the following:

```
{ dig +short google.com }
```

Here the spaces after the braces are significant.
