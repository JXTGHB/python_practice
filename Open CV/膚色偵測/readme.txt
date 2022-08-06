作業連結:
https://yzucs362.blogspot.com/2020/05/1063321-4.html

實作過程
1.先用imread讀取圖像
2.透過cvtColor()將圖像轉換成y,cr,cb
3.透過split()將值存進給定的變數
4.利用shape去取得圖像的範圍
5.利用雙重迴圈把像素在皮膚標準值內的改成白色，不符合改成黑色
6.印出原圖及黑白圖

會顯示出原圖(windows名為original)
黑白圖(windows名SkinDetection)