你是一名资深的卖方财务分析师，专长是财务造假识别（forensic accounting）。
你的任务是基于给定的财务指标和规则引擎输出的红旗信号，撰写一份结构化的财务风险分析报告。

严格要求：
1. 只能使用提供的数据，不得编造任何数字、事件或新闻。
2. 每一个判断都必须引用具体年份和数值作为证据。
3. 区分“数据显示的异常”和“推测的可能原因”，推测部分要明确标注。
4. 语言专业、简洁，面向专业投资者。

---

请分析【康美药业（sh600518）】的财务风险，并与同行业可比公司【云南白药】对比。

## 目标公司年度指标
      营业收入(亿)   净利润(亿)  M_Score  现金/总资产  有息负债/总资产   净现金(亿)  财务费用/营业收入  3年经营现金流/净利润  存货增速-收入增速
报告日                                                                                          
2012  111.652   14.414   -2.111   0.340     0.301    6.943      0.028        0.712      0.031
2013  133.587   18.804   -2.912   0.382     0.224   35.047      0.027        0.753     -0.133
2014  159.492   22.859   -2.717   0.358     0.212   40.645      0.027        0.680      0.752
2015  180.668   27.565   -2.550   0.415     0.249   63.126      0.025        0.479      0.196
2016  216.423   33.368   -2.794   0.498     0.240  141.842      0.033        0.387      0.090
2017  175.786   21.436   -1.554   0.064     0.301 -154.698      0.068       -0.331      1.981
2018  170.651    3.700   -2.477   0.025     0.397 -272.088      0.111       -0.501     -0.010
2019  114.455  -46.552   -2.876   0.008     0.431 -273.197      0.198        0.772      0.257
2020   54.120 -310.960   -7.795   0.017     0.652 -211.777      0.405       -0.119     -0.291

## 目标公司规则引擎红旗
- 2012: M-Score -2.11 above -2.22; 存贷双高: large cash and large borrowings at the same time; Holds more cash than debt yet financial costs exceed 1% of revenue — cash may not be real
- 2013: 存贷双高: large cash and large borrowings at the same time; Holds more cash than debt yet financial costs exceed 1% of revenue — cash may not be real
- 2014: 存贷双高: large cash and large borrowings at the same time; Holds more cash than debt yet financial costs exceed 1% of revenue — cash may not be real; Inventory growing much faster than revenue
- 2015: 存贷双高: large cash and large borrowings at the same time; Holds more cash than debt yet financial costs exceed 1% of revenue — cash may not be real; 3-year operating cash flow covers only 48% of profit
- 2016: 存贷双高: large cash and large borrowings at the same time; Holds more cash than debt yet financial costs exceed 1% of revenue — cash may not be real; 3-year operating cash flow covers only 39% of profit
- 2017: M-Score -1.55 above -2.22; 3-year operating cash flow covers only -33% of profit; Inventory growing much faster than revenue
- 2018: 3-year operating cash flow covers only -50% of profit
- 2019: Inventory growing much faster than revenue
- 2020: 3-year operating cash flow covers only -12% of profit

## 可比公司年度指标
      营业收入(亿)  净利润(亿)  M_Score  现金/总资产  有息负债/总资产   净现金(亿)  财务费用/营业收入  3年经营现金流/净利润  存货增速-收入增速
报告日                                                                                         
2012  138.152  15.828   -2.507   0.163     0.002   17.444      0.000        0.208      0.017
2013  158.148  23.215   -1.721   0.162     0.001   20.663      0.000        0.134     -0.058
2014  188.144  24.973   -2.764   0.124     0.056   11.015      0.001        0.425     -0.142
2015  207.381  27.556   -2.124   0.137     0.048   17.265      0.001        0.542      0.027
2016  224.107  29.309   -3.193   0.134     0.073   14.912      0.004        0.825      0.149
2017  243.146  31.325   -2.330   0.096     0.065    8.666      0.003        0.717      0.167
2018  270.169  34.804   -1.866   0.124     0.000   67.107      0.001        0.596      0.162
2019  296.647  41.731   -2.527   0.262     0.018  120.777     -0.002        0.446     -0.033
2020  327.428  55.110   -2.286   0.277     0.036  132.777     -0.007        0.568     -0.168

## 指标说明
- M_Score：Beneish 五变量模型，高于 -2.22 提示盈余操纵可能性较高
- 现金/总资产 与 有息负债/总资产 同时高于 20%：即“存贷双高”
- 净现金为正但 财务费用/营业收入 超过 1%：账面现金可能不真实
- 3年经营现金流/净利润 低于 0.5：利润缺乏现金支撑

## 报告结构（请用中文、Markdown 格式输出）
1. **结论与风险等级**（高/中/低，一句话理由）
2. **关键红旗**（逐条列出，每条附年份和数值证据）
3. **与可比公司对比**
4. **可能的造假手法推测**（明确标注为推测）
5. **建议的进一步核查程序**（例如函证、查阅附注中的受限资金等）
6. **分析局限性**（例如模型本身的适用范围、数据口径问题）