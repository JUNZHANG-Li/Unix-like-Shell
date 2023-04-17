grammar command ;

command_eof_nl   : command | command EOF | command NEWLINE ;

command       : call | command semicolon command | command double_amphersand command | command double_pipe command | pipe ;
pipe          : call pipe_op call | pipe pipe_op call ;

call          : whitespace+ (redirection whitespace+)* argument (whitespace+ atom)* whitespace+
              | whitespace+ (redirection whitespace+)* argument (whitespace+ atom)*
              | (redirection whitespace+)* argument (whitespace+ atom)* whitespace+
              | (redirection whitespace+)* argument (whitespace+ atom)*
              ;
atom          : redirection | argument ;
argument      : (quoted | unquoted)+ ;
redirection   : LANGLE whitespace+ argument 
              | RANGLE whitespace+ argument
              | LANGLE argument
              | RANGLE argument
              ;

pipe_op       : PIPE ;
semicolon     : SEMICOLON ;
double_amphersand : DOUBLE_AMPHERSAND ;
double_pipe : DOUBLE_PIPE ;
whitespace    : WHITESPACE ;
unquoted      : UNQUOTED ;
quoted        : single_quoted | double_quoted | back_quoted ;
single_quoted : '\'' (UNQUOTED | NONKEYWORD | SQCONTENT | '"' | '`' | '|' | ';' | '&&' | '||' | WHITESPACE+)+ '\'' ;
back_quoted   : '`' (UNQUOTED | NONKEYWORD | DQCONTENT | BQCONTENT | '\'' | '"' | '|' | ';' | '&&' | '||' | WHITESPACE+)+ '`' ;
double_quoted : '"' (back_quoted | DQCONTENT | UNQUOTED | NONKEYWORD | '`' | '\'' | '|' | ';' | '&&' | '||' | WHITESPACE+)+ '"' ;

//CHARACTER
LANGLE               : '<' ;
RANGLE               : '>' ;
DOUBLE_AMPHERSAND    : '&&';
DOUBLE_PIPE          : '||';
SEMICOLON            : ';' ;
PIPE                 : '|' ;
SINGLEQUOTE          : '\'';
DOUBLEQUOTE          : '"' ;
BACKQUOTE            : '`' ;
WHITESPACE           : (' '|'\t') ;
NEWLINE              : ('\r'? '\n' | '\r')+ ;

//CONTENTS
UNQUOTED             : ~[ \t'"`\n\r;|<>] ;
NONKEYWORD           : ~[\n\r'"`;|] ; 
DQCONTENT            : ~[\r\n"`] ;
BQCONTENT            : ~[\r\n`] ;
SQCONTENT            : ~[\r\n'] ; 