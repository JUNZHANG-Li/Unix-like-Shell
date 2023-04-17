# Additional Features

In the COMP0010 Shell, we have extended the shell to incorporate **History Substitution** and **Auto-Completion**.

# Features
## History Substitution
Allows the substitution of the current command with previously executed commands by using the 'up' and 'down' arrow keys

#### Usage:

Use 'up' and 'down' key to cycle through previously executed commands

#### Example Usage:

At command prompt `{some_directory}>`, pressing the 'up' arrow key at input prompt substitutes the current command with last command executed

## Auto-Completion
Enables Auto-completing the current input with a file or directory that starts with the current input, if there is more than one matching all matching files 
and directories are printed to the shell instead.

#### Usage: 

At prompt, enter a string to be extended, then auto-complete it by pressing `TAB`

#### Example usage:

Let `dir` contain the following files: {aaa, aad, bbb}

At command prompt `dir> `, typing 'a' then pressing tab, prints all the files and directories that start with 'a' to the shell that is `aaa  aad` and prompts the next command

At command prompt `dir> `, typing 'b' then pressing tab, auto-completes 'b', that is extend 'b' to 'bbb'
