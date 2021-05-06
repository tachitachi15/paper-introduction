## 概要
* wide-area surveillance radar(監視用のレーダー)でドップラースプレッドの性質を使って遠方に存在する歩行者を測定することが目標
* 歩行者のようなターゲットは腕、足、動体などが異なる速度で動くためrange-doppler-mapに単一の点ではなく線のような形で観測される。（ドップラースプレッド）
* 既存の手法はドップラースプレッドの性質を測定精度向上のために使えていない
* ordered statical constant false alarm rate(OS-CFAR)をドップラースプレッドターゲット向けに調整した方法を提案（CFARはノイズ電力によらない一定の値の閾値を与えてピークかどうか判定する方法）


## 導入
* FMCWレーダーはパルスレーダーに比べて低電力、変調の簡単さ、信号処理のシンプルさ、速度と距離を同時に測定できるメリットがある
* 監視レーダーや自動運転とかのレーダーにとって歩行者は重要なターゲットだが遠くにいる場合検出が困難
- 歩行者はRCS(radar cross section:レーダー有効断面積)が$1m^2$で低い　→　受信電力が低くなり検知が困難
- 監視レーダーではそもそも送信電力をあまり大きくできない

* 2D-FFTを基に2D-CFAR[16]が提案されているがターゲットが歩行者などのドップラースプレッドターゲットに対しては不適切なアプローチ
* Hough Transformを使ってRange Doppler Mapから歩行者ターゲットに対応する直線を検出して、直線上の電力を合計して検出能力を高める

## 論文の内容
* FMCWレーダーでの測定について
    - 波形
    - 信号処理
    - ドップラースプレッド特性
* CFAR法での検出
    - ドップラースプレッドターゲットの検出方法
    - OS-CFAR法
* 性能評価
    - 同様のシチュエーションを想定している[16]の方法と比較
    - 検出能力についての考察


## FMCWレーダーでの測定
### チャープ波形
24GHzのLFM-FMCWレーダーを使用
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

### 信号処理
* Fig1みたいに2D-FFTにかけて距離、速度を検出する。
* 縦方向のFFTで距離、横方向のFFTで速度を検出
* RDMのサイズ　$512 \times 512$ 

### ドップラースプレッド
 1ターゲットがRDMの1点に対応しているが、automotive-radar,wide-area surveillance radarのように高い分解能をもつレーダーでは歩行者のようなターゲットは1点ではなく線のように検出される。図３みたいな感じになる。

 図２のレーダー(24GHz,最大検出距離600m)で実際に検証した結果でも確認済み

 図４からドップラースプレッド特性は距離や速度に関係なく常に維持されている。

## CFAR法での検出
OS-CFAR(orderd statical-constant false alarm rate)をドップラースプレッドターゲット向けに調整した提案手法をここで紹介。
### ドップラースプレッドターゲットの検出方法


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

$H_0$の元で$Y_n>T_n$となる確率は（棄却率）

$$
    P_{fa} = \int_{T_n}^{\infty} p(Y_n|H_0) dY_n
$$

要求する$P_{fa}$の値から$T_n$が得られる。$T_n$を使って検出確率は

$$
    P_d = \int_{T_n}^{\infty} p(Y_n|H_1) dY_n
$$

### ドップラースプレッドターゲットをOS-CFARで検出する方法
閾値$T_n$をどうやって決めるか？この決め方にCFARの特徴が現れる。

CFARは主に
* CA-CFAR(cell average constant false alarm rate)
* OS-CFAR(order static constant false alarm rate)←一般的にこっちの方が性能が良いっていう論文が何個かあった

の二種類に分類される。

CA-CFARはマルチターゲット環境ではあまり良くない。
本論文ではOS-CFARを採用している。

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

$$
    \begin{aligned}
    p_{m}(y)=& m\left(\begin{array}{c}
    2 \times n_{1} \\
    m
    \end{array}\right)\left(1-\frac{\gamma\left(D, \frac{y}{\sigma_{n}^{2}}\right)}{\Gamma(D)}\right)^{2 \times n_{1}-m} \\
    & \cdot\left(\frac{\gamma\left(D, \frac{y}{\sigma_{n}^{2}}\right)}{\Gamma(D)}\right)^{m-1} \frac{(y)^{(D-1)} e^{-\frac{y}{\sigma_{n}^{2}}}}{\sigma_{n}^{2 D} \Gamma(D)}
    \end{aligned}
$$
$P_{fa}$は

$$
    \begin{aligned}
    P_{\mathrm{fa}}=& P\left[Y_{n} \geq \alpha_{\mathrm{OS}} \cdot \mathrm{Z}\right] \\
    =& \int_{0}^{+\infty} P\left[Y_{n} \geq \alpha_{\mathrm{OS}} \cdot y\right] p_{m}(y) d y \\
    =& m\left(\begin{array}{c}
    2 \times n_{1} \\
    m
    \end{array}\right) \int_{0}^{+\infty}\left(1-\frac{\gamma\left(D, \frac{\alpha_{0 s} \cdot y}{\sigma_{n}^{2}}\right)}{\Gamma(D)}\right) \\
    & \times\left(1-\frac{\gamma\left(D, \frac{y}{\sigma_{n}^{2}}\right)}{\Gamma(D)}\right)^{2 \times n_{1}-m}\left(\frac{\gamma\left(D, \frac{y}{\sigma_{n}^{2}}\right)}{\Gamma(D)}\right)^{m-1} \\
    & \times \frac{(y)^{(D-1)} e^{-\frac{y}{\sigma_{n}^{2}}}}{\sigma_{n}^{2 D} \Gamma(D)} d y \\
    =& m \binom{2\times n_1}{m} \int_{0}^{+\infty}\left(1-\frac{\gamma\left(D, \alpha_{\mathrm{OS}} \cdot u\right)}{\Gamma(D)}\right) \\
    & \times\left(1-\frac{\gamma(D, u)}{\Gamma(D)}\right)^{2 \times n_{1}-m}\left(\frac{\gamma(D, u)}{\Gamma(D)}\right)^{m-1} \\
    & \times \frac{(u)^{(D-1)} e^{-u}}{\Gamma(D)} d u .
    \end{aligned}
$$
$u=\frac{y}{\sigma_n^2}$で置換
多分論文の二項係数だったところが$(2\times n_1 m)$になってるのはミス。

この式から$P_{fa}$は平均ノイズ電力$\sigma_n^2$に依存しないので、提案手法はCFARの性質を満たしている。


## 性能

図6は$\sigma_n^2=1$,$\sigma_s^2=10$,$D=10$に設定
* (a)が[16]で使われていた指数分布に従う確率密度関数
* (b)が論文で提案されていた自由度2Dの$\chi^2$分布に従う確率密度関数

(a),(b)を比較すると(b)の方が$H_0$,$H_1$を分離できている。

図7はターゲットの検出確率の比較
図8のように自由度2Dが上がるほど検出確率は高くなっている。

$P_{fa}$を決めて(22)から$a_{OS}$を決定するので$a_{OS}$は$m,D$に依存する。この計算は時間がかかるが、ノイズ電力に依存する物ではないので予めレーダーシステムに組みこむことが可能

Table2は$P_{fa}=10^{-6}$に設定した時の$a_{OS}$

図10の提案手法(a)(b)の違い
* (a)はドップラーセルをD個のグループに分けて足していく
* (b)はドップラーセルをグループに分けず、スライドさせて足していく

$Y_n$と$T_n$の比率は

$$
    \mathrm{ratio} = \frac{Y_n}{a_{OS}Z}
$$
$\mathrm{ratio}<1$の時はターゲットが検出不能であり、ratioはターゲット検出能力の指標となる。

[17]から従来のOS-CFARアルゴリズムでは$a_{OS}=56.6$に設定されているが提案手法の方では$D=10$で$a_{OS}=3.9$

図11から提案手法(a)(b)に大差はないが、どちらも従来のOS-CFARの性能を上回っている。数値が変動しているのはターゲットのRCS(レーダー有効断面積)が変化しているからだが、どのアプローチでも条件は同じなのでアプローチ間の比較には影響はない。

図12は提案手法(a)でDを変化させてターゲットの検出能力を示している。D=50の時がD=10の時より検出能力という点で優れている訳ではない。これは歩行者の反射点の強さが大きく異なるから。(図13は提案手法(b)の場合)


図14からはD=10が一番実現可能な値だがこの値は速度分解能の値に大きく依存する。

監視レーダーはネットワークの一部となっているため特に誤検出を減らすことが重要
* 誤検出の大きな原因は木など
* 速度分解能をあげることで、止まっているターゲットと歩行者のようなゆっくり動くターゲットを分離できる。

図15は誤検出のことは考えずに速度分解能による比較を行った結果




