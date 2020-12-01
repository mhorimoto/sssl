# SSSL
Shock Stocker Serial Logger

ピエゾ素子を使って発電した電気をコンデンサにチャージしてそのチャージされた電圧をADCで観測する。
これで、衝撃の量を測る。

2020/12/02から鹿児島大学への道中で試験した。

## send-ssdata.py

衝撃測定装置から上がってきたデータを採取して上流になげる。

## send-location.py

GPSで取得した位置情報と時刻をagri-eyeサーバのWeb-API宛に送信する。
