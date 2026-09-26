# AIコンパニオン：新興する証拠、未解決の課題、そして責任ある設計への道

## 著者

Jeffrey T. Hancock, Stanford University
Diyi Yang, Stanford University
Dora Zhao, Stanford University
Yutong Zhang, Stanford University
Robert E. Kraut, Carnegie Mellon University
Evan Frondorf, Anthropic
Ryn Linthicum, Anthropic

## ワークショップ主催者

Ruopeng An, New York University
Nathan Berl, Character.AI
Eisha Buch, Common Sense Media
Matthew R. DeVerna, Stanford University
Nathanael J. Fast, University of Southern California
Dylan Hadfield-Menell, Massachusetts Institute of Technology
Jodi Halpern, University of California, Berkeley
Karen Jusko, OpenAI
Pat Kilby, Eyes on Health
Sunnie S. Y. Kim, Microsoft Research
Sunny Liu, Stanford University
Kim Malfacini, OpenAI
Ryan K. McBain, RAND
Sanyam Mehra, Meta
Jared Moore, Stanford University
Desmond C. Ong, The University of Texas at Austin
Pat Pataranutaporn, MIT Media Lab
Roma Patel, Google DeepMind
Lonnie Shumsky, Stanford University
Ranjit Singh, Data & Society
Maxwelle Sokol, Ever AI
Cori Stott, Digital Wellness Lab at Boston Children's Hospital
Jina Suh, Microsoft Research
Lisa Titus, Meta

## ワークショップ参加者（姓のアルファベット順）

Nestor Maslej, Stanford University
Kelsey Prater, Spoke Consulting
Jacy Reese Anthis, Stanford University
Pub Archiwaranguprok, MIT Media Lab
Anthony Baez, Massachusetts Institute of Technology
Bingxu Han, Stanford University
Sheer Karny, MIT Media Lab
Levi Morris Lebovitz, Stanford University
RT Rogers, Stanford University
Yuewen Yang, Stanford University
Peggy Yin, Stanford University

## ワークショップ記録係

---

## 目次

- エグゼクティブサマリー … 3
- 主要な要点 … 4
- 序論 … 5
- AIコンパニオンの定義 … 6
  - チャットボットとバーチャルアバターにおけるAIコンパニオンシップを可能にする特性
- 利用データ … 11
- 利点と害 … 13
  - 潜在的な利点
  - 潜在的な害
- ワークショップの主要テーマ … 19
  - 基本事項：役割、限界、基準
  - 技術的デザイン上の課題
  - ユーザー保護と文脈
- 合意と対立の一般的な領域 … 25
  - 合意の領域
  - 緊張の領域
- 研究の課題、優先事項、次のステップ … 28
  - 研究の課題
  - 研究の優先事項
- 分野横断的な責任と要点 … 30
  - ガバナンスの課題の枠組み
  - 産業の責任：安全な設計、適切なインセンティブ、運用上の保護
  - 学術の責任：証拠、測定、概念的明確さ
  - 市民社会の責任：規範設定、提言、ユーザー中心の保護
  - 政策立案者の考慮事項：ガードレール、基準、説明責任
  - 分野横断的な広範な要点
- 謝辞 … 35
- 参考文献 … 37

---

## エグゼクティブサマリー

AIコンパニオンは、ユーザーがAIシステムを単なるツールとしてだけでなく、情緒的サポート、伴走、メンターシップ、ロールプレイ、親密さの源としても関わる、新たな相互作用の形態として急速に台頭している。これらのシステムは一部のユーザーにとって利点をもたらす可能性がある一方で、ウェルビーイング、社会的関係、ユーザーの安全への影響、そしてそれらがどのように設計・保護・統治されるべきかという重要な課題も提起している。利用の拡大と公的な関心の高まりにもかかわらず、実証研究は技術開発の速度に追いついておらず、利点、害、効果的な保護策に関する多くの重要な問いが未解決かつ未研究のままである。本報告書は、Stanford Tech Impact & Policy Centerが主催し、Anthropicと共催した学際的ワークショップの議論を統合したものである。研究者、産業実務者、市民社会組織が集まり、新興する合意の領域、未解決の課題、そして今後の研究とガバナンスの優先事項を特定した。

### 本報告書の引用方法

Yutong Zhang, Dora Zhao, Nestor Maslej, Matthew R. DeVerna, Ruopeng An, Nathan Berl, Eisha Buch, Nathanael J. Fast, Dylan Hadfield-Menell, Jodi Halpern, Karen Jusko, Pat Kilby, Sunnie S. Y. Kim, Sunny Liu, Kim Malfacini, Ryan K. McBain, Sanyam Mehra, Jared Moore, Desmond C. Ong, Pat Pataranutaporn, Roma Patel, Lonnie Shumsky, Ranjit Singh, Maxwelle Sokol, Cori Stott, Jina Suh, Lisa Titus, Ryn Linthicum, Evan Frondorf, Robert E. Kraut, Diyi Yang, Jeffrey T. Hancock. "AI Companions: Emerging Evidence, Open Questions, and Paths Toward Responsible Design." The Tech Impact and Policy Center, Stanford University, Stanford, CA, September 2026.

本報告書「AI Companions: Emerging Evidence, Open Questions, and Paths Toward Responsible Design」は、Attribution-NoDerivatives 4.0 International ライセンスの下に提供される。

---

## 主要な要点

**1. AIコンパニオンシップは製品カテゴリではなく、利用のモードである。** AIコンパニオンシップは、専用コンパニオンアプリやそれにマーケティングされたものに限定されない。コンパニオン的な相互作用は、専用コンパニオンシステムだけでなく、関係的目的で使われる汎用チャットボットを通じても生じうる。AIコンパニオンシップは、システムの設計だけでなく、ユーザーがこれらのシステムとどのように関わり、どのように解釈するかによっても形作られる。したがって、AIコンパニオンシップを理解するには、技術的デザイン特性、文脈、利用パターンへの注意が必要である。

**2. AIコンパニオンは、意味のある機会と意味のあるリスクの両方を提示する。** AIコンパニオンは、情緒的サポート、アイデンティティの探求、社会的リハーサルなどの利点をもたらす可能性がある。同時に、依存、社会的孤立、操作、歪んだ関係期待に関する懸念も存在する。利点に寄与しうる同じ特性が、害にも寄与しうる。既存の証拠は依然として限られており、全体的な利点と害について明確な合意は現在ない。

**3. 異なるコンパニオン利用ケースには、異なる保護策が必要である。** AIコンパニオンシステムは、設計、意図された目的、利用パターンにおいて異なる。AIシステムが情緒的サポート、伴走、恋愛ロールプレイ、その他の機微な領域に使用される場合、主にチューター、スキル構築、その他の支援形態に使用される場合よりも、より強い保護策を要する可能性がある。効果的な保護策は、ユーザーの年齢、脆弱性、利用文脈に敏感であるべきであり、異なるユーザーや相互作用には異なる保護が必要であることを認識すべきである。どの保護策が適切であり、保護と自律性をどのようにバランスさせるかという重要な問いは依然として残されている。

**4. AIコンパニオンは、人間関係を補完すべきであり、代替すべきではない。** AIコンパニオンは、学習、内省、情緒的サポート、社会的練習の機会を提供できる。しかし、人間関係の代替となるよう設計されるべきではない。責任あるコンパニオンの設計は、意図的な利用を促し、他者とのつながりを支援し、AIコンパニオンがユーザーの人生において果たす役割围绕う明確な境界を強化すべきである。コンパニオンシステムは、健全な関与を促し、人間関係を代替するのではなく補完するときに、これらの目標をよりよく支援できる。

**5. AIコンパニオンのガバナンスには、分野横断的な共有責任が必要である。** AIコンパニオンに対する責任は、単一のアクターを超えて及ぶ。基盤モデル開発者、コンパニオンアプリ提供者、プラットフォーム・デバイス運営者、研究者、市民社会組織、政策立案者、ユーザーはすべて、AIコンパニオンの開発と影響を形作る上で役割を果たしている。中心的な課題は、AIエコシステム全体で役割をどのように配分し、異なるリスクに対処するためにどのアプローチが最も効果的かを決定することである。これらの課題に対処するには、さらなる研究、分野横断的な調整、単一の介入への依存ではなく、補完的なアプローチの組み合わせが必要である。

---

## 序論

AIコンパニオンシステムは、ニッチなアプリケーションから広く利用される消費者技術へと急速に移行してきた。人々は、Character.AIやReplikaのような専用AIコンパニオンプラットフォーム、あるいはClaude、ChatGPT、Geminiのような汎用チャットボットを使用して、友情、メンターシップ、恋愛関係、情緒的サポートに似た相互作用を行っている。これらのシステムの多くは主にコンパニオンシップ用途のために設計されていないものの、汎用AIシステムとの関係的相互作用はますます顕著になっている。しかし、その普及にもかかわらず、AIコンパニオンシップとは何か、これらのシステムが実際にはどのように使用されているか、そしてそれらの短期的・長期的な心理的・社会的・安全上の含意がどのようなものかについて、共有された理解は依然として限られている。さらに、AIロールプレイとコンパニオンシップに関する研究は学問分野をまたいで断片化しており、コンパニオンとその影響に関する実証文献は依然として萌芽期にある。その結果、利点と害がどのように分布しているか、誰が最も影響を受けるか、安全上の責任をAIエコシステム全体でどのように配分すべきかについて、明確な合意はない。

本論文は、2025年11月17日にStanford Universityで開催された学際的ワークショップから生まれたものであり、これらのギャップに対処することを目的としている。ワークショップには、学術界、産業界、市民社会からの研究者が集まった。参加者は定義に関する問いへの見解を共有し、利用と結果に関する新興する実証証拠を検討し、AIコンパニオンエコシステム全体における既存の安全プラクティスを検討し、技術的デザイン上の課題を議論し、適切なユーザー保護を探った。ワークショップではまた、リスクの軽減と有益な結果の促進に対する責任が、基盤モデル提供者、下流のチャットボット開発者、独立した研究者、市民社会組織の間でどのように分かれているかが明示的に検討された。

本報告書は、AIコンパニオン围绕うワークショップの議論、新興する証拠、専門家の見解、対立の領域を統合し、現在何が知られているか、何が不確実であるか、そしてこの分野を前進させるために何が必要かを明確にするものである。本論文は主にワークショップの議論に従うが、場合によっては外部の実証研究に言及する。本報告書に示された見解は、ワークショップの議論と関連する証拠の統合を反映しており、必ずしもすべてのワークショップ参加者やその所属組織の見解を反映するものではない。より具体的には、本論文は(1) AIコンパニオンシップのためのより明確な概念的・定義的基盤を確立し、(2) AIコンパニオンが実際にはどのように使用されているかに関する利用可能なデータを要約する（関与のパターンと規模を含む）、(3) 潜在的な利点と害に関する証拠の現状を評価し、ユーザー、文脈、利用パターンによって結果が異なることを認識するデュアルユースの枠組みを採用し、(4) ワークショップの議論中に特定された主要テーマ、合意の領域、緊張の点を浮き彫りにし、(5) 産業、学術界、市民社会、政策立案者に対する優先的な研究方向と分野横断的な責任を明確にする。ワークショップでは成人と若者の両方に関するAIコンパニオンシップの問題が検討されたが、それがワークショップの焦点ではなかった。したがって、本報告書は成人と若者の両方の文脈でAIコンパニオンを扱うが、成人からの知見は若者に転移できないことを強調する。最後に、単一の規範的立場を提唱するのではなく、本論文は、AIコンパニオンシステムに関連する今後の実証研究、責任ある設計、ガバナンスの取り組みを情報提供できる共有された分析的枠組みを提供することを意図している。
