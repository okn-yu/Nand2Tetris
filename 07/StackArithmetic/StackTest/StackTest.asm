@256
D=A
@SP
M=D
@17
D=A
@256
M=D
@SP
M=M+1
@17
D=A
@257
M=D
@SP
M=M+1
@SP
M=M-1
@257
D=M
@SP
M=M-1
@256
D=M-D
@SP
M=M+1
@SP
M=M-1
@34
D;JEQ
@256
M=0
@36
0;JMP
@256
M=-1
@SP
M=M+1
@17
D=A
@257
M=D
@SP
M=M+1
@16
D=A
@258
M=D
@SP
M=M+1
@SP
M=M-1
@258
D=M
@SP
M=M-1
@257
D=M-D
@SP
M=M+1
@SP
M=M-1
@68
D;JEQ
@257
M=0
@70
0;JMP
@257
M=-1
@SP
M=M+1
@16
D=A
@258
M=D
@SP
M=M+1
@17
D=A
@259
M=D
@SP
M=M+1
@SP
M=M-1
@259
D=M
@SP
M=M-1
@258
D=M-D
@SP
M=M+1
@SP
M=M-1
@102
D;JEQ
@258
M=0
@104
0;JMP
@258
M=-1
@SP
M=M+1
@892
D=A
@259
M=D
@SP
M=M+1
@891
D=A
@260
M=D
@SP
M=M+1
@SP
M=M-1
@260
D=M
@SP
M=M-1
@259
D=M-D
@SP
M=M+1
@SP
M=M-1
@136
D;JLT
@259
M=0
@138
0;JMP
@259
M=-1
@SP
M=M+1
@891
D=A
@260
M=D
@SP
M=M+1
@892
D=A
@261
M=D
@SP
M=M+1
@SP
M=M-1
@261
D=M
@SP
M=M-1
@260
D=M-D
@SP
M=M+1
@SP
M=M-1
@170
D;JLT
@260
M=0
@172
0;JMP
@260
M=-1
@SP
M=M+1
@891
D=A
@261
M=D
@SP
M=M+1
@891
D=A
@262
M=D
@SP
M=M+1
@SP
M=M-1
@262
D=M
@SP
M=M-1
@261
D=M-D
@SP
M=M+1
@SP
M=M-1
@204
D;JLT
@261
M=0
@206
0;JMP
@261
M=-1
@SP
M=M+1
@32767
D=A
@262
M=D
@SP
M=M+1
@32766
D=A
@263
M=D
@SP
M=M+1
@SP
M=M-1
@263
D=M
@SP
M=M-1
@262
D=M-D
@SP
M=M+1
@SP
M=M-1
@238
D;JGT
@262
M=0
@240
0;JMP
@262
M=-1
@SP
M=M+1
@32766
D=A
@263
M=D
@SP
M=M+1
@32767
D=A
@264
M=D
@SP
M=M+1
@SP
M=M-1
@264
D=M
@SP
M=M-1
@263
D=M-D
@SP
M=M+1
@SP
M=M-1
@272
D;JGT
@263
M=0
@274
0;JMP
@263
M=-1
@SP
M=M+1
@32766
D=A
@264
M=D
@SP
M=M+1
@32766
D=A
@265
M=D
@SP
M=M+1
@SP
M=M-1
@265
D=M
@SP
M=M-1
@264
D=M-D
@SP
M=M+1
@SP
M=M-1
@306
D;JGT
@264
M=0
@308
0;JMP
@264
M=-1
@SP
M=M+1
@57
D=A
@265
M=D
@SP
M=M+1
@31
D=A
@266
M=D
@SP
M=M+1
@53
D=A
@267
M=D
@SP
M=M+1
@SP
M=M-1
@267
D=M
@SP
M=M-1
@266
M=M+D
@SP
M=M+1
@112
D=A
@267
M=D
@SP
M=M+1
@SP
M=M-1
@267
D=M
@SP
M=M-1
@266
M=M-D
@SP
M=M+1
@SP
M=M-1
@266
D=M
M=-D
@SP
M=M+1
@SP
M=M-1
@266
D=M
@SP
M=M-1
@265
M=M&D
@SP
M=M+1
@82
D=A
@266
M=D
@SP
M=M+1
@SP
M=M-1
@266
D=M
@SP
M=M-1
@265
M=M|D
@SP
M=M+1
@SP
M=M-1
@265
D=M
M=!D
@SP
M=M+1
