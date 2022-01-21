---
title: Use Curly Braces While Pasting Shell Commands
date: 2021-11-08
---

Pasting shell commands can be a pain when they include hidden return `\n` characters. In such a case, your shell will try to execute the command immediately. To prevent that, use curly braces `{ <cmd> }` while pasting the command. Your command
should look like the following:

```bash
{ dig +short google.com }
```

Here the spaces after the braces are significant.