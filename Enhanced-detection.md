## abstract 
* 歩行者のようなターゲットはrange-doppler-mapに単一の点ではなく線のような形で観測される。　腕、足、動体などが異なる速度で動くため
* 既存の手法はドップラースプレッドの性質を測定精度向上のために使えていない
* ordered statical constant false alarm rateをドップラースプレッドターゲット向けに調整した方法を提案
* wide-area surveillance radar(監視用のレーダー)を使ってドップラースプレッドの性質を使って遠方に存在する歩行者を測定することが目標

## introduction
* FMCWレーダーはパルスレーダーに比べて低電力、変調の簡単さ、信号処理のシンプルさ、速度と距離を同時に測定できるメリットがある
* 監視レーダーや自動運転とかのレーダーにとって歩行者は重要なターゲットだが遠くにいる場合検出が困難
- 歩行者はRCS(radar cross section:レーダー有効断面積)が$1m^2$で低い　→　受信電力が低くなり検知が困難
- 監視レーダーではそもそも送信電力をあまり大きくできない

* 2D-FFTを基に2D-CFAR(constant false alarm rate)[16]が提案されているがターゲットが歩行者などのドップラースプレッドターゲットに対しては不適切なアプローチ
* Hough Transformを使ってRange Doppler Mapから歩行者ターゲットに対応する直線を検出して、直線上の電力を合計して検出能力を高める

## Chirp Sequence Waveform
### Chirp Sequence Waveform
* $24$GHzのwide-area surveillance radar (LFM FMCW)を使用
* beat frequency$f_B$は

$$ 
    f_B = -\frac{f_{sweep}}{T_{chirp}} \frac{2}{c}R - \frac{2}{\lambda}v_r = f_R + f_D
$$

* $f_{sweep}$:変調帯域幅, $T_{chirp}$:1チャープあたりの時間 $f_R$:距離による周波数差、$f_D$:速度による周波数差

* $T_{chirp}$が小さい場合or$f_{sweep}$が大きい場合は$f_R$の影響が支配的になり
    
$$
    f_B \approx -\frac{f_{sweep}}{T_{chirp}} \frac{2}{c}R
$$
* LFM波形の場合$v$を測定するためにチャープを$L$回を送信するからミキシング後の信号は

$$
    s(t,l) = \mathrm{exp}(j2\pi(f_Bt-f_DlT_{chirp}+\varphi))
$$

* 一般的に歩行者の動きのモデルは５つのパーツからの反射を想定しているので（腕、足、胴体）歩行者から得られる信号は

$$
    s(t,l) = \sum_{k=1}^{K} \mathrm{exp}(j2\pi(f_Bt-f_{D_k}lT_{chirp}+\varphi_{k}))
$$

### Signal Processing Procedure

