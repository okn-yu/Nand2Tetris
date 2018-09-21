# 第4章
HACK機械語の説明および簡単なHACK機械語でのプログラムを実装する  

### 機械語
・機械語の仕様はハードウェアのアーキテクチャ（CPU/ALU/アセンブラ/メインメモリのアドレス長）と対応している  
・機械語が命令セットとCPUの命令セットは一致する  
・そのためCPUが異なれば機械語の命令セットも異なる  
・CPUのサポートしていない命令はソフトウェア側で実装する

### 感想
・アセンブラでの実装に意外に苦戦した。アセンブリ言語が大変な理由の一つはロジックを視覚的に把握できないからだと思う。  
・高級水準言語ならひと目で分かるバグもアセンブリ言語だとステップ実行しないと気づけない。