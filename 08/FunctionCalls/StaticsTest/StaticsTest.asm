@261
D=A
@SP
M=D
(Sys.init)
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
@Class1.set$retAddr-1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(Class1.set$retAddr-1)
@SP
M=M-1
A=M
D=M
@R5
M=D
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
@Class2.set$retAddr-1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(Class2.set$retAddr-1)
@SP
M=M-1
A=M
D=M
@R5
M=D
@Class1.get$retAddr-1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(Class1.get$retAddr-1)
@Class2.get$retAddr-1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
D=D-1
D=D-1
D=D-1
D=D-1
D=D-1
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(Class2.get$retAddr-1)
(WHILE)
@WHILE
0;JMP
(Class1.set)
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@Class1.vm.0
M=D
@ARG
A=M
A=A+1
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@Class1.vm.1
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@FRAME
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@RETURN
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@FRAME
A=M
A=A-1
D=M
@THAT
M=D
@FRAME
A=M
A=A-1
A=A-1
D=M
@THIS
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
D=M
@ARG
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@RETURN
A=M
0;JMP
(Class1.get)
@Class1.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@Class1.vm.1
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
@LCL
D=M
@FRAME
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@RETURN
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@FRAME
A=M
A=A-1
D=M
@THAT
M=D
@FRAME
A=M
A=A-1
A=A-1
D=M
@THIS
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
D=M
@ARG
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@RETURN
A=M
0;JMP
(Class2.set)
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@Class2.vm.0
M=D
@ARG
A=M
A=A+1
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@Class2.vm.1
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@FRAME
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@RETURN
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@FRAME
A=M
A=A-1
D=M
@THAT
M=D
@FRAME
A=M
A=A-1
A=A-1
D=M
@THIS
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
D=M
@ARG
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@RETURN
A=M
0;JMP
(Class2.get)
@Class2.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1
@Class2.vm.1
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@SP
M=M-1
@SP
A=M
M=M-D
@SP
M=M+1
@LCL
D=M
@FRAME
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@RETURN
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@FRAME
A=M
A=A-1
D=M
@THAT
M=D
@FRAME
A=M
A=A-1
A=A-1
D=M
@THIS
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
D=M
@ARG
M=D
@FRAME
A=M
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@RETURN
A=M
0;JMP
