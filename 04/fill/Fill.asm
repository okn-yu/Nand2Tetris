// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// INIT SCR_END=24575
@24575
D=A
@SCR_END
M=D

(LOOP)

// INIT SCR_ADDR=16384
@16384
D=A
@SCRADDR
M=D

@KBD
D=M
@LOOP_WHITE
D;JEQ

(LOOP_BLACK)

@SCRADDR
A=M
M=-1
A=A+1
D=A
@SCRADDR
M=D

@SCR_END
D=M-D

@LOOP_BLACK
D;JGE

@LOOP
0;JMP

(LOOP_WHITE)

@SCRADDR
A=M
M=0
A=A+1
D=A
@SCRADDR
M=D

@SCR_END
D=M-D

@LOOP_WHITE
D;JGE

@LOOP
0;JMP