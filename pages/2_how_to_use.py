import streamlit as st

st.title('TableOneの使い方')

st.subheader('''
1. アップロードするファイルについて
ファイルは整形済みのexcelまたはcsvのみをアップロードすることができます。
ここで「整形済み」とは、データ型の統一、カテゴリカル変数をbooleanまたは[0,1]のフラグ形式にしたものをいいます。
3カテゴリー以上の変数についてはone-hot表現にしてください。
Stringで入ったカテゴリ変数については後日version updateにて対応します。
''')

st.subheader('''
2. 曝露因子の選択について
曝露因子となるカテゴリー変数を選択します。
ここで選択した曝露因子をもとに、tableは全患者、曝露有りの患者、曝露無しの患者の3列で構成されます。
''')

st.subheader('''
3. 変数選択について
連続変数とカテゴリー変数をそれぞれ選択します。
その後、Table 1に上から表示したい順に選択して下さい。
''')

st.subheader('''
4. P-valueについて
曝露有りの患者群と無しの患者群について、連続変数はt-検定を、カテゴリ変数はfisher's exact検定を行っています。
その他の検定については後日のversion updateで対応します。
''')