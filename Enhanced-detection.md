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
$24$GHzのwide-area surveillance radar (LFM FMCW)を使用
 beat frequency$f_B$は

$$ 
    f_B = -\frac{f_{sweep}}{T_{chirp}} \frac{2}{c}R - \frac{2}{\lambda}v_r = f_R + f_D
$$

 $f_{sweep}$:変調帯域幅, $T_{chirp}$:1チャープあたりの時間 $f_R$:距離による周波数差、$f_D$:速度による周波数差

 $T_{chirp}$が小さい場合or$f_{sweep}$が大きい場合は$f_R$の影響が支配的になり
    
$$
    f_B \approx -\frac{f_{sweep}}{T_{chirp}} \frac{2}{c}R
$$
 LFM波形の場合$v$を測定するためにチャープを$L$回を送信するからミキシング後の信号は

$$
    s(t,l) = \mathrm{exp}(j2\pi(f_Bt-f_DlT_{chirp}+\varphi))
$$

 一般的に歩行者の動きのモデルは５つのパーツからの反射を想定しているので（腕、足、胴体）歩行者から得られる信号は

$$
    
    s(t,l) = \sum_{k=1}^{K} \mathrm{exp}(j2\pi(f_Bt-f_{D_k}lT_{chirp}+\varphi_{k}))
$$

### Signal Processing Procedure
* Fig1みたいに2D-FFTにかけて距離、速度を検出する。
* 縦方向のFFTで距離、横方向のFFTで速度を検出
* RDMのサイズ　$512 \times 512$ 

### Doppler Spread Characteristic
 1ターゲットがRDMの1点に対応しているが、automotive-radar,wide-area surveillance radarのように高い分解能をもつレーダーでは歩行者のようなターゲットは1点ではなく線のように検出される。図３みたいな感じになる。

 図２のレーダー(24GHz,最大検出距離600m)で実際に検証した結果でも確認済み

* $f_{PRF} = 1$kHzで$L=512$,ドップラー分解能が$\Delta f = f_{PRF}/L$

* ドップラー周波数が$f_d = 2v/\lambda$なので検出可能速度は[-3.125,3.125]

* 人の歩行速度は大体1.5m/sだから検出できる

 図４からドップラースプレッド特性は距離や速度に関係なく常に維持されている。

## Adaptive CFAR Detection of Doppler Spread Targets

### Doppler-Spread Target Dtection Procedure
OS-CFAR(orderd statical-constant false alarm rate)をドップラースプレッドターゲット向けに調整した提案手法をここで紹介。

 Hough変換で線を検出して各ドップラービンを加算していくのがメインアイデア(図5)

$$
    Y_n = \sum_{d=0}^{D-1}|x_{n,l+d}|^2
$$

 $x_{n,l}$:RDMの各要素(FFT後の結果)、n:距離インデックス、l:ドップラーインデックス,D:ドップラースプレッドが占めるセル数

 $Y_n$を$[n-n_1,n+n_1]$の範囲に渡って求める。

ターゲット推定は仮説検定に基づいて行う。
- $H_0$:帰無仮説　ここではターゲットが存在せずノイズのみの状況
- $H_1$:対立仮説　ターゲットが存在する状況 

$T_n$をテストセル内で計算された閾値をすると$Y_n \geq T_n$ならターゲット、$Y_n < T_n$ならノイズと判定できる。

$H_0$ではノイズのみ。$Y_n$はD個のi.i.dかつ平均0,分散$\sigma^2_n$の複素ガウス変数の2乗和になる。$E_n = 2Y_n/\sigma_n^2$とすると$E_n$は自由度2Dの$\chi^2$分布に従う。

$$
    p(E_n|H_0) = \frac{E_n^{(D-1)}e^{-\frac{E_n}{2}}}{2^D \Gamma(D)}
$$

累積分布関数は

$$
    P_{E_n}(E_n|H_0) = \frac{\gamma(D,\frac{E_n}{2})}{\Gamma(D)}
$$

$\gamma(s,x)$は不完全ガンマ関数の積分区間が[0,x]の方

$$
    \gamma(s,x) = \int_{0}^{x} t^{s-1} e^{-t} dt
$$
累積分布関数を微分してノイズだけの場合の確率密度関数が得られる。

$$
    p(Y_n|H_0) = 
    \frac{
        \left(
            \frac{2Y_n}{\sigma_n^2}
        \right)^{(D-1)}
        e^{
            -\frac{
                \left(
                    \frac{2Y_n}{\sigma_n^2}
                \right)}
            {2}
        }
    }
    {2^D \Gamma(D)}
    \frac{2}{\sigma^2}

    = \frac{Y_n^{(D-1)}e^{-\frac{Y_n}{\sigma_n^2}}}{\sigma_n^{2D} \Gamma(D)}
$$

$Y_n$の累積分布関数は

$$
    P_{Y_n}(E_n|H_0) = \frac{\gamma(D,\frac{Y_n}{\sigma_n^2})}{\Gamma(D)}
$$

対立仮説$H_1$のターゲットがある場合は、信号電力を平均0,分散$\sigma^2$(実部、虚部それぞれ$\sigma^2/2$)とすると

確率密度関数は

$$
    p(Y_n|H_1) = \frac{Y_n^{(D-1)}e^{-\frac{Y_n}{\sigma_n^2 + \sigma_s^2}}}{(\sigma_s^2+\sigma_n^2)^{D} \Gamma(D)}
$$

累積分布関数は

$$
    P_{Y_n}(Y_n|H_1) = \frac{\gamma(D,\frac{Y_n}{\sigma_n^2+\sigma_s^2})}{\Gamma(D)}
$$

ネイマンピアソンの基準[34]によると

$$
    P_{fa} = \int_{T_n}^{\infty} p(Y_n|H_0) dY_n
$$

要求する$P_{fa}$の値から$T_n$が得られる。$T_n$を使って検出確率は

$$
    P_d = \int_{T_n}^{\infty} p(Y_n|H_1) dY_n
$$

### Doppler-Spread Target OS-CFAR Detection Procedure

CA-CFAR(cell average constant false alarm rate)はマルチターゲット環境ではあまり良くないがOS-CFARを元にすればより耐性が強くなる。

OS-CFARを使うために、$[Y_{n-n_1},...,Y_{n-1},Y_{n+1},...,Y_{n+n_1}]$を昇順に並べる。

$$
    Y_{(1)} < Y_{(2)} < ... < Y_{(m)} <...<Y_{(2\times n_1)}
$$

OS-CFARの中心となる考えはノイズとクラッター(地面とかからの余分な信号）を表す閾値にm番目のセルを使うことで

$$
    Z = Y_{(m)}
$$

クラッターとノイズ電力の平均は$Z$にthreshold factor$a_{OS}$を乗算することで得られて。

$$
    P_{fa} = P[Y_n \geq a_{OS}Z]
$$

これを計算するのに$Z$の確率密度関数を知る必要がある。順序統計量のm番目の変数の確率密度関数は[35]より

$$
    p_m(y) = m \binom{2n_1}{m}(1-P_{Y_n}(Y_n|H_0))^{2n_1-m}P_{Y_n}(Y_n|H_0)^{m-1}p(Y_n|H_0)
$$








