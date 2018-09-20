**■NANDゲートの定義**  
a nand b = not (a and b)  
  
**■NOTゲートの導出**  
not a = not (a and a)  
      = (a nand a)  
  
**■ANDゲートの導出**  
a and b =  not (not (a and b))  
        = (not (a and b))) nand (not (a and b)))  
        = (a nand b) nand (a nand b)  
  
**■ORゲートの導出**  
a or b = not ((not a) and (not b))  
       = (not a) nand (not b)  
       = (a nand a) nand (b nand b)  
  
**■XORゲートの導出**  
a xor b = ((not a) and b) or (a and (not b))  
  
**■マルチプレクサゲートの導出**  
out = (a and (not b) and (not sel)) or (a and b and (not sel)) or ((not a) and b and sel) or (a and b and sel)  
  
前2つの項  
= a and ((not b) or b) and (not sel)  
= a and (not sel)  
  
後2つの項  
= ((not a) and b and sel) or (a and b and sel)  
= ((not a) or a) and b and sel  
= b and sel  
  
合わせると  
out = (a and (not sel)) or (b and sel)  
  
**■デマルチプレクサゲートの導出**  
outA = (in and (not sel)  
outB = (in and sel)  
  
**■各論理ゲート作成に必要なNANDゲートの本数**  
NOTゲート：1本  
ANDゲート：3本  
ORゲート：3本  
XORゲート：11本  
  
**■Project01で作成したゲート一覧**  
・Notゲート  
・Andゲート  
・Orゲート  
・Xorゲート  
・多ビットNot/And/Or/Xorゲート  
・マルチプレクサゲート  
・多ビットマルチプレクサゲート  
・デマルチプレクサゲート  
・多ビットデマルチプレクサゲート    
