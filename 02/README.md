# 第2章
加算器を用いてALUの実装を行う

### 加算器 
加算器は「半加算器」「全加算器」「多ビット加算器」の3種類からなる
- 半加算器(2bit加算器)：2入力(a,b)2出力(sum,carry)  
- 全加算器(3bit加算器)：3入力(a,b,c)2出力(sum,carry）  
- 多ビット加算器(nbit加算器)：2入力(a,b)1出力(sum)  
  
### ALU(算術論理演算機)  
- HACK用のALUはハードウェアとしては加算・減算・論理積・論理和・ビット反転・符号反転をサポート  
- 浮動小数点および乗除算はソフトウェアで対応する
- zx, nx, zy, ny, f, noを1つずつ実装すれば自然にALUが完成する