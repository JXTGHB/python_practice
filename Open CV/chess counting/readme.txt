
三、實作方法：
1.imread讀取照片(利用迴圈一張一張做)
2.將照片轉成灰階
3.利用高斯模糊去除雜訊
4.利用canny去擷取圖像邊緣
5.threshold二值化後用findContours去找出棋子
6.利用count變數去計算數量
最後分別write出有標示棋子位置的圖片
