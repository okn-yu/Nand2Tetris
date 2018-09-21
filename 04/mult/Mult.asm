// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@2
M=0 // R2=0

(LOOP)
@1
D=M // D=R1
@END // A=ADDR(END)
D;JLE // if D=<0 then goto END
@1
M=M-1 //R1-=1
@0
D=M // D=R0
@2
M=M+D // R2+=R0
@LOOP 
0;JMP // goto LOOP

(END)
@END
0;JMP
