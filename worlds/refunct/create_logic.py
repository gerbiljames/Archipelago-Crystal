
import json

log_data_vanilla_1 = \
"""
Sending location checks: [10012102]
Sending location checks: [10012103]
Sending location checks: [10012102]
Sending location checks: [10012008]
Sending location checks: [10012110]
Sending location checks: [10012109]
Sending location checks: [10012110]
Sending location checks: [10012109]
Sending location checks: [10012001]
Sending location checks: [10012006]
Sending location checks: [10013003]
Sending location checks: [10012202]
Sending location checks: [10013003]
Sending location checks: [10012006]
Sending location checks: [10012005]
Sending location checks: [10012010]
Sending location checks: [10012009]
Sending location checks: [10012108]
Sending location checks: [10012008]
Sending location checks: [10012110]
Sending location checks: [10012008]
Sending location checks: [10012010]
Sending location checks: [10012005]
Sending location checks: [10012006]
Sending location checks: [10013001]
Sending location checks: [10013003]
Sending location checks: [10012202]
Sending location checks: [10013003]
Sending location checks: [10013001]
Sending location checks: [10013002]
Sending location checks: [10013013]
Sending location checks: [10013006]
Sending location checks: [10012201]
Sending location checks: [10013006]
Sending location checks: [10013014]
Sending location checks: [10012909]
Sending location checks: [10012910]
Sending location checks: [10012912]
Sending location checks: [10012911]
Sending location checks: [10012913]
Sending location checks: [10012914]
Sending location checks: [10012408]
Sending location checks: [10012404]
Sending location checks: [10011401]
Sending location checks: [10011301]
Sending location checks: [10001301]
Sending location checks: [10011301]
Sending location checks: [10011501]
Sending location checks: [10010303]
Sending location checks: [10011501]
Sending location checks: [10010207]
Sending location checks: [10010202]
Sending location checks: [10010304]
Sending location checks: [10011005]
Sending location checks: [10011005]
Sending location checks: [10010102]
Sending location checks: [10010202]
Sending location checks: [10010206]
Sending location checks: [10010207]
Sending location checks: [10011504]
Sending location checks: [10011403]
Sending location checks: [10011504]
Sending location checks: [10011703]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10010408]
Sending location checks: [10010406]
Sending location checks: [10010506]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10012801]
Sending location checks: [10010408]
Sending location checks: [10010104]
Sending location checks: [10010406]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010605]
Sending location checks: [10010605]
Sending location checks: [10010407]
Sending location checks: [10010605]
Sending location checks: [10010602]
Sending location checks: [10010602]
Sending location checks: [10010602]
Sending location checks: [10010604]
Sending location checks: [10010808]
Sending location checks: [10010807]
Sending location checks: [10010904]
Sending location checks: [10010905]
Sending location checks: [10010806]
Sending location checks: [10010803]
Sending location checks: [10010805]
Sending location checks: [10010809]
Sending location checks: [10010603]
Sending location checks: [10011811]
Sending location checks: [10011808]
Sending location checks: [10011811]
Sending location checks: [10010802]
Sending location checks: [10010801]
Sending location checks: [10010802]
Sending location checks: [10011808]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010506]
Sending location checks: [10010406]
Sending location checks: [10010104]
Sending location checks: [10010104]
Sending location checks: [10010105]
Sending location checks: [10010102]
Sending location checks: [10010102]
Sending location checks: [10010202]
Sending location checks: [10010206]
Sending location checks: [10010207]
Sending location checks: [10011504]
Sending location checks: [10011403]
Sending location checks: [10011403]
Sending location checks: [10012705]
Sending location checks: [10012703]
Sending location checks: [10012609]
Sending location checks: [10002601]
Sending location checks: [10012611]
Sending location checks: [10012610]
Sending location checks: [10012602]
Sending location checks: [10012406]
Sending location checks: [10012402]
Sending location checks: [10012409]
Sending location checks: [10011301]
Sending location checks: [10001301]
Sending location checks: [10011301]
Sending location checks: [10012404]
Sending location checks: [10012408]
Sending location checks: [10012407]
Sending location checks: [10012914]
Sending location checks: [10012913]
Sending location checks: [10012911]
Sending location checks: [10012904]
Sending location checks: [10002901]
Sending location checks: [10012910]
Sending location checks: [10013014]
Sending location checks: [10013002]
Sending location checks: [10013001]
Sending location checks: [10012001]
Sending location checks: [10012109]
Sending location checks: [10012110]
Sending location checks: [10012102]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012102]
Sending location checks: [10012103]
Sending location checks: [10012102]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012104]
Sending location checks: [10012108]
Sending location checks: [10011903]
Sending location checks: [10011902]
Sending location checks: [10011901]
Sending location checks: [10010908]
Sending location checks: [10010907]
Sending location checks: [10011902]
Sending location checks: [10010910]
Sending location checks: [10010907]
Sending location checks: [10010908]
Sending location checks: [10010907]
Sending location checks: [10010910]
Sending location checks: [10010909]
Sending location checks: [10010910]
Sending location checks: [10010907]
Sending location checks: [10010908]
Sending location checks: [10011901]
Sending location checks: [10011107]
Sending location checks: [10011104]
Sending location checks: [10010303]
Sending location checks: [10010202]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010807]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010903]
Sending location checks: [10010901]
Sending location checks: [10010902]
Sending location checks: [10010901]
Sending location checks: [10010903]
Sending location checks: [10010905]
Sending location checks: [10010903]
Sending location checks: [10010901]
Sending location checks: [10010902]
Sending location checks: [10011004]
Sending location checks: [10011006]
Sending location checks: [10011008]
Sending location checks: [10011006]
Sending location checks: [10011008]
Sending location checks: [10011007]
Sending location checks: [10011008]
Sending location checks: [10011006]
Sending location checks: [10011004]
Sending location checks: [10010902]
Sending location checks: [10010906]
Sending location checks: [10011002]
Sending location checks: [10011006]
Sending location checks: [10011007]
Sending location checks: [10011005]
Sending location checks: [10010304]
Sending location checks: [10010304]
Sending location checks: [10011005]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010605]
Sending location checks: [10010605]
Sending location checks: [10010402]
Sending location checks: [10010401]
Sending location checks: [10010204]
Sending location checks: [10010408]
Sending location checks: [10010406]
Sending location checks: [10010404]
Sending location checks: [10010407]
Sending location checks: [10010605]
Sending location checks: [10010601]
Sending location checks: [10011803]
Sending location checks: [10011803]
Sending location checks: [10010703]
Sending location checks: [10010704]
Sending location checks: [10010703]
Sending location checks: [10011807]
Sending location checks: [10011806]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011810]
Sending location checks: [10011809]
Sending location checks: [10010505]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011810]
Sending location checks: [10011809]
Sending location checks: [10010505]
Sending location checks: [10010503]
Sending location checks: [10010504]
Sending location checks: [10010501]
Sending location checks: [10000501]
Sending location checks: [10012813]
Sending location checks: [10012813]
Sending location checks: [10010505]
Sending location checks: [10010501]
Sending location checks: [10010503]
Sending location checks: [10010504]
Sending location checks: [10012812]
Sending location checks: [10012802]
Sending location checks: [10012802]
Sending location checks: [10012812]
Sending location checks: [10010504]
Sending location checks: [10010503]
Sending location checks: [10010505]
Sending location checks: [10011809]
Sending location checks: [10011810]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011809]
Sending location checks: [10011810]
Sending location checks: [10011809]
Sending location checks: [10010505]
Sending location checks: [10010506]
Sending location checks: [10010407]
Sending location checks: [10010605]
Sending location checks: [10010602]
Sending location checks: [10010107]
Sending location checks: [10011009]
Sending location checks: [10010807]
Sending location checks: [10011009]
Sending location checks: [10010807]
Sending location checks: [10010806]
Sending location checks: [10010803]
Sending location checks: [10010805]
Sending location checks: [10010811]
Sending location checks: [10010805]
Sending location checks: [10010810]
Sending location checks: [10010604]
Sending location checks: [10010808]
Sending location checks: [10010604]
Sending location checks: [10010602]
Sending location checks: [10010402]
Sending location checks: [10010409]
Sending location checks: [10010403]
Sending location checks: [10010405]
Sending location checks: [10010403]
Sending location checks: [10010401]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010201]
Sending location checks: [10010307]
Sending location checks: [10010306]
Sending location checks: [10010305]
Sending location checks: [10010306]
Sending location checks: [10010307]
Sending location checks: [10010201]
Sending location checks: [10010307]
Sending location checks: [10010306]
Sending location checks: [10010308]
Sending location checks: [10001101]
Sending location checks: [10011205]
Sending location checks: [10012201]
Sending location checks: [10013006]
Sending location checks: [10013014]
Sending location checks: [10013002]
Sending location checks: [10013001]
Sending location checks: [10012001]
Sending location checks: [10012006]
Sending location checks: [10013003]
Sending location checks: [10012202]
Sending location checks: [10013003]
Sending location checks: [10012006]
Sending location checks: [10012005]
Sending location checks: [10012008]
Sending location checks: [10012110]
Sending location checks: [10012008]
Sending location checks: [10012010]
Sending location checks: [10012009]
Sending location checks: [10012108]
Sending location checks: [10012009]
Sending location checks: [10011901]
Sending location checks: [10011902]
Sending location checks: [10010910]
Sending location checks: [10010909]
Sending location checks: [10010910]
Sending location checks: [10010907]
Sending location checks: [10010907]
Sending location checks: [10010908]
Sending location checks: [10011901]
Sending location checks: [10011107]
Sending location checks: [10011104]
Sending location checks: [10010303]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010406]
Sending location checks: [10010506]
Sending location checks: [10010408]
Sending location checks: [10011603]
Sending location checks: [10011703]
Sending location checks: [10011603]
Sending location checks: [10012801]
Sending location checks: [10010408]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10011501]
Sending location checks: [10010303]
Sending location checks: [10011108]
Sending location checks: [10001101]
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10012201]
Sending location checks: [10012201]
Sending location checks: [10013006]
Sending location checks: [10013013]
Sending location checks: [10013002]
Sending location checks: [10013001]
Sending location checks: [10013003]
Sending location checks: [10012202]
Sending location checks: [10013003]
Sending location checks: [10012006]
Sending location checks: [10012005]
Sending location checks: [10012010]
Sending location checks: [10012009]
Sending location checks: [10011003]
Sending location checks: [10011901]
Sending location checks: [10010908]
Sending location checks: [10010907]
Sending location checks: [10010910]
Sending location checks: [10010907]
Sending location checks: [10010908]
Sending location checks: [10010907]
Sending location checks: [10011902]
Sending location checks: [10011903]
Sending location checks: [10011905]
Sending location checks: [10001901]
Sending location checks: [10011905]
Sending location checks: [10012113]
Sending location checks: [10012107]
Sending location checks: [10012110]
Sending location checks: [10012109]
Sending location checks: [10012001]
Sending location checks: [10013001]
Sending location checks: [10013003]
Sending location checks: [10012202]
Sending location checks: [10011102]
Sending location checks: [10011103]
Sending location checks: [10011105]
Sending location checks: [10010303]
Sending location checks: [10010202]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010103]
Sending location checks: [10010104]
Sending location checks: [10010105]
Sending location checks: [10010202]
Sending location checks: [10010105]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010105]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010106]
Sending location checks: [10010106]
Sending location checks: [10010103]
Sending location checks: [10010104]
Sending location checks: [10010207]
Sending location checks: [10010104]
Sending location checks: [10010105]
Sending location checks: [10010202]
Sending location checks: [10010303]
Sending location checks: [10010202]
Sending location checks: [10010304]
Sending location checks: [10010202]
Sending location checks: [10010102]
Sending location checks: [10010303]
Sending location checks: [10010102]
Sending location checks: [10010303]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010406]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010604]
Sending location checks: [10010106]
Sending location checks: [10010103]
Sending location checks: [10010104]
Sending location checks: [10010207]
Sending location checks: [10011703]
Sending location checks: [10010207]
Sending location checks: [10011501]
Sending location checks: [10010207]
Sending location checks: [10010202]
Sending location checks: [10010207]
Sending location checks: [10010202]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010202]
Sending location checks: [10010303]
Sending location checks: [10011501]
Sending location checks: [10010207]
Sending location checks: [10010303]
Sending location checks: [10011501]
Sending location checks: [10011401]
Sending location checks: [10011501]
Sending location checks: [10010303]
Sending location checks: [10011501]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10010202]
Sending location checks: [10010206]
Sending location checks: [10010207]
Sending location checks: [10010202]
Sending location checks: [10010206]
Sending location checks: [10010206]
Sending location checks: [10010206]
Sending location checks: [10010207]
Sending location checks: [10010104]
Sending location checks: [10010105]
Sending location checks: [10010202]
Sending location checks: [10010304]
Sending location checks: [10010202]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010207]
Sending location checks: [10011504]
Sending location checks: [10010207]
Sending location checks: [10011703]
Sending location checks: [10010207]
Sending location checks: [10011703]
Sending location checks: [10011603]
Sending location checks: [10011703]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10010207]
Sending location checks: [10010104]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10010406]
Sending location checks: [10010104]
Sending location checks: [10010105]
Sending location checks: [10010202]
Sending location checks: [10010303]
Sending location checks: [10011108]
Sending location checks: [10010303]
Sending location checks: [10011108]
Sending location checks: [10010308]
Sending location checks: [10011108]
Sending location checks: [10010303]
Sending location checks: [10011501]
Sending location checks: [10010303]
Sending location checks: [10010303]
Sending location checks: [10010207]
Sending location checks: [10010303]
Sending location checks: [10010202]
Sending location checks: [10010303]
Sending location checks: [10010202]
Sending location checks: [10010303]
Sending location checks: [10011104]
Sending location checks: [10010303]
Sending location checks: [10011104]
Sending location checks: [10011106]
Sending location checks: [10011104]
Sending location checks: [10010303]
Sending location checks: [10010202]
Sending location checks: [10010304]
Sending location checks: [10010202]
Sending location checks: [10010304]
Sending location checks: [10011005]
Sending location checks: [10010309]
Sending location checks: [10011005]
Sending location checks: [10010304]
Sending location checks: [10011005]
Sending location checks: [10010309]
Sending location checks: [10010304]
Sending location checks: [10010202]
Sending location checks: [10010206]
Sending location checks: [10011501]
Sending location checks: [10010303]
Sending location checks: [10011104]
Sending location checks: [10010303]
Sending location checks: [10011105]
Sending location checks: [10010303]
Sending location checks: [10011103]
Sending location checks: [10011105]
Sending location checks: [10010303]
Sending location checks: [10010202]
Sending location checks: [10010202]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010404]
Sending location checks: [10010104]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10010406]
Sending location checks: [10010506]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10011603]
Sending location checks: [10010408]
Sending location checks: [10012801]
Sending location checks: [10010408]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010605]
Sending location checks: [10010407]
Sending location checks: [10010605]
Sending location checks: [10010605]
Sending location checks: [10010603]
Sending location checks: [10010605]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010808]
Sending location checks: [10010604]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010807]
Sending location checks: [10010604]
Sending location checks: [10010806]
Sending location checks: [10010807]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010904]
Sending location checks: [10010905]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010904]
Sending location checks: [10010905]
Sending location checks: [10010903]
Sending location checks: [10010903]
Sending location checks: [10010905]
Sending location checks: [10010806]
Sending location checks: [10010803]
Sending location checks: [10010806]
Sending location checks: [10010803]
Sending location checks: [10010803]
Sending location checks: [10010805]
Sending location checks: [10010805]
Sending location checks: [10010804]
Sending location checks: [10010801]
Sending location checks: [10010804]
Sending location checks: [10010801]
Sending location checks: [10010802]
Sending location checks: [10010801]
Sending location checks: [10010802]
Sending location checks: [10011811]
Sending location checks: [10010802]
Sending location checks: [10010701]
Sending location checks: [10011811]
Sending location checks: [10010802]
Sending location checks: [10011811]
Sending location checks: [10010701]
Sending location checks: [10010802]
Sending location checks: [10011811]
Sending location checks: [10010603]
Sending location checks: [10011811]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010602]
Sending location checks: [10010601]
Sending location checks: [10000601]
Sending location checks: [10010601]
Sending location checks: [10010604]
Sending location checks: [10010602]
Sending location checks: [10010601]
Sending location checks: [10000601]
Sending location checks: [10010601]
Sending location checks: [10011803]
Sending location checks: [10010505]
Sending location checks: [10011805]
Sending location checks: [10011810]
Sending location checks: [10011809]
Sending location checks: [10011804]
Sending location checks: [10010505]
Sending location checks: [10010501]
Sending location checks: [10000501]
Sending location checks: [10012813]
Sending location checks: [10010505]
Sending location checks: [10011806]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011806]
Sending location checks: [10011805]
Sending location checks: [10011807]
Sending location checks: [10000701]
Sending location checks: [10010701]
Sending location checks: [10010702]
Sending location checks: [10010702]
Sending location checks: [10010801]
Sending location checks: [10010804]
Sending location checks: [10010801]
Sending location checks: [10010801]
Sending location checks: [10010802]
Sending location checks: [10011811]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010604]
Sending location checks: [10010604]
Sending location checks: [10010604]
Sending location checks: [10010106]
Sending location checks: [10010106]
Sending location checks: [10010103]
Sending location checks: [10010104]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10010406]
Sending location checks: [10010506]
Sending location checks: [10010506]
Sending location checks: [10010404]
Sending location checks: [10010506]
Sending location checks: [10010406]
Sending location checks: [10010104]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010605]
Sending location checks: [10010407]
Sending location checks: [10010605]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010808]
Sending location checks: [10010604]
Sending location checks: [10010602]
Sending location checks: [10010605]
Sending location checks: [10010605]
Sending location checks: [10010602]
Sending location checks: [10010602]
Sending location checks: [10010602]
Sending location checks: [10010808]
Sending location checks: [10010809]
Sending location checks: [10011811]
Sending location checks: [10010802]
Sending location checks: [10010801]
Sending location checks: [10010702]
Sending location checks: [10000702]
Sending location checks: [10010702]
Sending location checks: [10010701]
Sending location checks: [10000701]
Sending location checks: [10010701]
Sending location checks: [10010802]
Sending location checks: [10010801]
Sending location checks: [10010801]
Sending location checks: [10010802]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010808]
Sending location checks: [10010809]
Sending location checks: [10010704]
Sending location checks: [10010703]
Sending location checks: [10010704]
Sending location checks: [10010703]
Sending location checks: [10011807]
Sending location checks: [10011806]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10010505]
Sending location checks: [10010501]
Sending location checks: [10010504]
Sending location checks: [10010503]
Sending location checks: [10010503]
Sending location checks: [10010504]
Sending location checks: [10010503]
Sending location checks: [10010505]
Sending location checks: [10011809]
Sending location checks: [10011808]
Sending location checks: [10011811]
Sending location checks: [10010802]
Sending location checks: [10010801]
Sending location checks: [10010802]
Sending location checks: [10011811]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010808]
Sending location checks: [10010806]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010903]
Sending location checks: [10010905]
Sending location checks: [10010904]
Sending location checks: [10010905]
Sending location checks: [10010903]
Sending location checks: [10010901]
Sending location checks: [10010903]
Sending location checks: [10010901]
Sending location checks: [10010903]
Sending location checks: [10010901]
Sending location checks: [10010902]
Sending location checks: [10010901]
Sending location checks: [10010902]
Sending location checks: [10011004]
Sending location checks: [10010902]
Sending location checks: [10010906]
Sending location checks: [10010902]
Sending location checks: [10011006]
Sending location checks: [10011008]
Sending location checks: [10011004]
Sending location checks: [10011008]
Sending location checks: [10011004]
Sending location checks: [10011006]
Sending location checks: [10011008]
Sending location checks: [10011006]
Sending location checks: [10011008]
Sending location checks: [10011006]
Sending location checks: [10011007]
Sending location checks: [10011006]
Sending location checks: [10011007]
Sending location checks: [10011005]
Sending location checks: [10011005]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010807]
Sending location checks: [10010904]
Sending location checks: [10010905]
Sending location checks: [10010903]
Sending location checks: [10010901]
Sending location checks: [10010902]
Sending location checks: [10011901]
Sending location checks: [10011003]
Sending location checks: [10011901]
Sending location checks: [10011902]
Sending location checks: [10011901]
Sending location checks: [10011003]
Sending location checks: [10012009]
Sending location checks: [10011003]
Sending location checks: [10012009]
Sending location checks: [10012010]
Sending location checks: [10012009]
Sending location checks: [10012108]
Sending location checks: [10012008]
Sending location checks: [10012108]
Sending location checks: [10012008]
Sending location checks: [10012110]
Sending location checks: [10012008]
Sending location checks: [10012102]
Sending location checks: [10012008]
Sending location checks: [10012102]
Sending location checks: [10012103]
Sending location checks: [10012102]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012102]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012104]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012106]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012106]
Sending location checks: [10012108]
Sending location checks: [10012106]
Sending location checks: [10012108]
Sending location checks: [10011903]
Sending location checks: [10012108]
Sending location checks: [10011903]
Sending location checks: [10011902]
Sending location checks: [10011903]
Sending location checks: [10011902]
Sending location checks: [10010910]
Sending location checks: [10011902]
Sending location checks: [10010910]
Sending location checks: [10010907]
Sending location checks: [10010910]
Sending location checks: [10010909]
Sending location checks: [10010910]
Sending location checks: [10011902]
Sending location checks: [10011903]
Sending location checks: [10011904]
Sending location checks: [10011903]
Sending location checks: [10011904]
Sending location checks: [10012113]
Sending location checks: [10011904]
Sending location checks: [10012114]
Sending location checks: [10011903]
Sending location checks: [10012114]
Sending location checks: [10012107]
Sending location checks: [10012114]
Sending location checks: [10012107]
Sending location checks: [10012113]
Sending location checks: [10012107]
Sending location checks: [10012113]
Sending location checks: [10012107]
Sending location checks: [10012113]
"""

log_data_vanilla_2 = """
Sending location checks: [10010102]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010106]
Sending location checks: [10010103]
Sending location checks: [10010104]
Sending location checks: [10010207]
Sending location checks: [10010104]
Sending location checks: [10010404]
Sending location checks: [10010104]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10011703]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10010205]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10010205]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10010104]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010105]
Sending location checks: [10010202]
Sending location checks: [10010304]
Sending location checks: [10010202]
Sending location checks: [10010304]
Sending location checks: [10010309]
Sending location checks: [10010304]
Sending location checks: [10010309]
Sending location checks: [10010304]
Sending location checks: [10010202]
Sending location checks: [10010303]
Sending location checks: [10010202]
Sending location checks: [10010102]
Sending location checks: [10010202]
Sending location checks: [10010304]
Sending location checks: [10010309]
Sending location checks: [10011005]
Sending location checks: [10010309]
Sending location checks: [10010309]
Sending location checks: [10011005]
Sending location checks: [10010309]
Sending location checks: [10011105]
Sending location checks: [10010303]
Sending location checks: [10011105]
Sending location checks: [10011103]
Sending location checks: [10011102]
Sending location checks: [10011103]
Sending location checks: [10011106]
Sending location checks: [10011104]
Sending location checks: [10010303]
Sending location checks: [10010102]
Sending location checks: [10010303]
Sending location checks: [10010202]
Sending location checks: [10010303]
Sending location checks: [10010202]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010104]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10010406]
Sending location checks: [10010506]
Sending location checks: [10010406]
Sending location checks: [10010506]
Sending location checks: [10010404]
Sending location checks: [10010406]
Sending location checks: [10010506]
Sending location checks: [10010406]
Sending location checks: [10010404]
Sending location checks: [10010406]
Sending location checks: [10010404]
Sending location checks: [10010502]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010506]
Sending location checks: [10010407]
Sending location checks: [10010605]
Sending location checks: [10010407]
Sending location checks: [10010605]
Sending location checks: [10010605]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010605]
Sending location checks: [10010602]
Sending location checks: [10010402]
Sending location checks: [10010401]
Sending location checks: [10010405]
Sending location checks: [10010403]
Sending location checks: [10010405]
Sending location checks: [10010403]
Sending location checks: [10010401]
Sending location checks: [10010403]
Sending location checks: [10010405]
Sending location checks: [10010401]
Sending location checks: [10010403]
Sending location checks: [10010401]
Sending location checks: [10010403]
Sending location checks: [10010409]
Sending location checks: [10010403]
Sending location checks: [10010405]
Sending location checks: [10010409]
Sending location checks: [10010403]
Sending location checks: [10010401]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10010401]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10010401]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010503]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010503]
Sending location checks: [10010502]
Sending location checks: [10010503]
Sending location checks: [10010504]
Sending location checks: [10010503]
Sending location checks: [10010501]
Sending location checks: [10010503]
Sending location checks: [10010505]
Sending location checks: [10010503]
Sending location checks: [10010505]
Sending location checks: [10011809]
Sending location checks: [10011810]
Sending location checks: [10011809]
Sending location checks: [10011810]
Sending location checks: [10011805]
Sending location checks: [10011810]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011809]
Sending location checks: [10011804]
Sending location checks: [10010505]
Sending location checks: [10011804]
Sending location checks: [10010505]
Sending location checks: [10011804]
Sending location checks: [10010505]
Sending location checks: [10000501]
Sending location checks: [10010501]
Sending location checks: [10010505]
Sending location checks: [10012813]
Sending location checks: [10010505]
Sending location checks: [10011806]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10010505]
Sending location checks: [10010501]
Sending location checks: [10010501]
Sending location checks: [10010503]
Sending location checks: [10010504]
Sending location checks: [10010503]
Sending location checks: [10010505]
Sending location checks: [10010503]
Sending location checks: [10010506]
Sending location checks: [10010407]
Sending location checks: [10010506]
Sending location checks: [10010407]
Sending location checks: [10010605]
Sending location checks: [10010103]
Sending location checks: [10010605]
Sending location checks: [10010407]
Sending location checks: [10010506]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010505]
Sending location checks: [10011805]
Sending location checks: [10011807]
Sending location checks: [10011807]
Sending location checks: [10010701]
Sending location checks: [10010802]
Sending location checks: [10010701]
Sending location checks: [10011811]
Sending location checks: [10010701]
Sending location checks: [10000701]
Sending location checks: [10010701]
Sending location checks: [10011811]
Sending location checks: [10010802]
Sending location checks: [10011811]
Sending location checks: [10010802]
Sending location checks: [10010801]
Sending location checks: [10010802]
Sending location checks: [10010801]
Sending location checks: [10010802]
Sending location checks: [10010701]
Sending location checks: [10010802]
Sending location checks: [10011811]
Sending location checks: [10010802]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010603]
Sending location checks: [10010802]
Sending location checks: [10011811]
Sending location checks: [10010603]
Sending location checks: [10010802]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010808]
Sending location checks: [10010604]
Sending location checks: [10010808]
Sending location checks: [10010809]
Sending location checks: [10010808]
Sending location checks: [10010809]
Sending location checks: [10010805]
Sending location checks: [10010809]
Sending location checks: [10010811]
Sending location checks: [10010809]
Sending location checks: [10010810]
Sending location checks: [10010811]
Sending location checks: [10000801]
Sending location checks: [10010811]
Sending location checks: [10010810]
Sending location checks: [10010811]
Sending location checks: [10000801]
Sending location checks: [10010811]
Sending location checks: [10010803]
Sending location checks: [10010805]
Sending location checks: [10010803]
Sending location checks: [10010805]
Sending location checks: [10010803]
Sending location checks: [10010806]
Sending location checks: [10010803]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010903]
Sending location checks: [10010901]
Sending location checks: [10010902]
Sending location checks: [10010906]
Sending location checks: [10011004]
Sending location checks: [10011006]
Sending location checks: [10011008]
Sending location checks: [10011004]
Sending location checks: [10011008]
Sending location checks: [10011004]
Sending location checks: [10010904]
Sending location checks: [10010807]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010903]
Sending location checks: [10010901]
Sending location checks: [10010902]
Sending location checks: [10010906]
Sending location checks: [10010906]
Sending location checks: [10010906]
Sending location checks: [10010906]
Sending location checks: [10011004]
Sending location checks: [10011008]
Sending location checks: [10011004]
Sending location checks: [10010908]
Sending location checks: [10010907]
Sending location checks: [10010908]
Sending location checks: [10010907]
Sending location checks: [10010910]
Sending location checks: [10010907]
Sending location checks: [10010910]
Sending location checks: [10011902]
Sending location checks: [10010910]
Sending location checks: [10011902]
Sending location checks: [10011903]
Sending location checks: [10011902]
Sending location checks: [10011903]
Sending location checks: [10011904]
Sending location checks: [10011903]
Sending location checks: [10011902]
Sending location checks: [10010907]
Sending location checks: [10010908]
Sending location checks: [10011901]
Sending location checks: [10011107]
Sending location checks: [10011901]
Sending location checks: [10011107]
Sending location checks: [10011106]
Sending location checks: [10011107]
Sending location checks: [10011104]
Sending location checks: [10011107]
Sending location checks: [10011001]
Sending location checks: [10011107]
Sending location checks: [10011001]
Sending location checks: [10001001]
Sending location checks: [10011001]
Sending location checks: [10011001]
Sending location checks: [10011001]
Sending location checks: [10011001]
Sending location checks: [10011001]
Sending location checks: [10011001]
Sending location checks: [10011001]
Sending location checks: [10011001]
Sending location checks: [10011001]
Sending location checks: [10011001]
Sending location checks: [10011001]
Sending location checks: [10010102]
"""

log_data_vanilla_3 = """
Sending location checks: [10010105]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010102]
Sending location checks: [10010303]
Sending location checks: [10011104]
Sending location checks: [10010303]
Sending location checks: [10011104]
Sending location checks: [10011001]
Sending location checks: [10011104]
Sending location checks: [10011001]
Sending location checks: [10001001]
Sending location checks: [10011001]
Sending location checks: [10011107]
Sending location checks: [10011901]
Sending location checks: [10011003]
Sending location checks: [10011901]
Sending location checks: [10011003]
Sending location checks: [10011107]
Sending location checks: [10011003]
Sending location checks: [10001002]
Sending location checks: [10012009]
Sending location checks: [10001002]
Sending location checks: [10011003]
Sending location checks: [10012009]
Sending location checks: [10012010]
Sending location checks: [10012009]
Sending location checks: [10012010]
Sending location checks: [10012005]
Sending location checks: [10012010]
Sending location checks: [10012008]
Sending location checks: [10012010]
Sending location checks: [10012008]
Sending location checks: [10012110]
Sending location checks: [10012008]
Sending location checks: [10012102]
Sending location checks: [10012103]
Sending location checks: [10012102]
Sending location checks: [10012103]
Sending location checks: [10012102]
Sending location checks: [10012110]
Sending location checks: [10012102]
Sending location checks: [10012110]
Sending location checks: [10012109]
Sending location checks: [10012110]
Sending location checks: [10012109]
Sending location checks: [10012001]
Sending location checks: [10012006]
Sending location checks: [10012005]
Sending location checks: [10012006]
Sending location checks: [10012001]
Sending location checks: [10012109]
Sending location checks: [10012110]
Sending location checks: [10012102]
Sending location checks: [10012103]
Sending location checks: [10012102]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012102]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012104]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012104]
Sending location checks: [10012108]
Sending location checks: [10002101]
Sending location checks: [10012108]
Sending location checks: [10012009]
Sending location checks: [10012108]
Sending location checks: [10012106]
Sending location checks: [10012108]
Sending location checks: [10012106]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012104]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012104]
Sending location checks: [10012114]
Sending location checks: [10012104]
Sending location checks: [10012114]
Sending location checks: [10012107]
Sending location checks: [10012114]
Sending location checks: [10012107]
Sending location checks: [10012113]
Sending location checks: [10012107]
Sending location checks: [10012113]
Sending location checks: [10011904]
Sending location checks: [10012113]
Sending location checks: [10011904]
Sending location checks: [10011902]
Sending location checks: [10010910]
Sending location checks: [10011902]
Sending location checks: [10010907]
Sending location checks: [10011902]
Sending location checks: [10010907]
Sending location checks: [10010910]
Sending location checks: [10010907]
Sending location checks: [10010908]
Sending location checks: [10011901]
Sending location checks: [10011003]
Sending location checks: [10011102]
Sending location checks: [10011103]
Sending location checks: [10011105]
Sending location checks: [10011103]
Sending location checks: [10011102]
Sending location checks: [10011103]
Sending location checks: [10011105]
Sending location checks: [10011101]
Sending location checks: [10011101]
Sending location checks: [10011105]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10011101]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10010308]
Sending location checks: [10011108]
Sending location checks: [10012304]
Sending location checks: [10011108]
Sending location checks: [10012304]
Sending location checks: [10012404]
Sending location checks: [10012304]
Sending location checks: [10012404]
Sending location checks: [10012304]
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10011205]
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10001101]
Sending location checks: [10011108]
Sending location checks: [10010308]
Sending location checks: [10011108]
Sending location checks: [10010308]
Sending location checks: [10011108]
Sending location checks: [10010303]
Sending location checks: [10011501]
Sending location checks: [10011401]
Sending location checks: [10011501]
Sending location checks: [10011401]
Sending location checks: [10011301]
Sending location checks: [10011401]
Sending location checks: [10012706]
Sending location checks: [10012705]
Sending location checks: [10012706]
Sending location checks: [10012705]
Sending location checks: [10012704]
Sending location checks: [10012705]
Sending location checks: [10012702]
Sending location checks: [10012706]
Sending location checks: [10012705]
Sending location checks: [10012705]
Sending location checks: [10012704]
Sending location checks: [10012702]
Sending location checks: [10012706]
Sending location checks: [10012705]
Sending location checks: [10012706]
Sending location checks: [10012705]
Sending location checks: [10011403]
Sending location checks: [10001401]
Sending location checks: [10011403]
Sending location checks: [10011504]
Sending location checks: [10011403]
Sending location checks: [10001401]
Sending location checks: [10011403]
Sending location checks: [10011501]
Sending location checks: [10011403]
Sending location checks: [10011501]
Sending location checks: [10011301]
Sending location checks: [10011401]
Sending location checks: [10011301]
Sending location checks: [10011401]
Sending location checks: [10012404]
Sending location checks: [10012304]
Sending location checks: [10012404]
Sending location checks: [10012304]
Sending location checks: [10011108]
Sending location checks: [10012304]
Sending location checks: [10011108]
Sending location checks: [10010308]
Sending location checks: [10011108]
Sending location checks: [10010308]
Sending location checks: [10011108]
Sending location checks: [10001101]
Sending location checks: [10011205]
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10001101]
Sending location checks: [10011108]
Sending location checks: [10012304]
Sending location checks: [10011108]
Sending location checks: [10012304]
Sending location checks: [10012404]
Sending location checks: [10012304]
Sending location checks: [10012404]
Sending location checks: [10011401]
Sending location checks: [10011301]
Sending location checks: [10011401]
Sending location checks: [10011301]
Sending location checks: [10011501]
Sending location checks: [10011403]
Sending location checks: [10011501]
Sending location checks: [10011403]
Sending location checks: [10001401]
Sending location checks: [10012705]
Sending location checks: [10001401]
Sending location checks: [10011403]
Sending location checks: [10012705]
Sending location checks: [10012706]
Sending location checks: [10011401]
Sending location checks: [10011301]
Sending location checks: [10011401]
Sending location checks: [10011501]
Sending location checks: [10011401]
Sending location checks: [10011501]
Sending location checks: [10010303]
Sending location checks: [10010207]
Sending location checks: [10010104]
Sending location checks: [10010404]
Sending location checks: [10010104]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10010205]
Sending location checks: [10010205]
Sending location checks: [10010205]
Sending location checks: [10011603]
Sending location checks: [10011703]
Sending location checks: [10011603]
Sending location checks: [10011703]
Sending location checks: [10011504]
Sending location checks: [10011703]
Sending location checks: [10011504]
Sending location checks: [10011703]
Sending location checks: [10011504]
Sending location checks: [10011403]
Sending location checks: [10001401]
Sending location checks: [10011403]
Sending location checks: [10012705]
Sending location checks: [10011403]
Sending location checks: [10012705]
Sending location checks: [10012704]
Sending location checks: [10012705]
Sending location checks: [10012704]
Sending location checks: [10012704]
Sending location checks: [10012703]
Sending location checks: [10012609]
Sending location checks: [10002601]
Sending location checks: [10012611]
Sending location checks: [10012610]
Sending location checks: [10012611]
Sending location checks: [10012610]
Sending location checks: [10012602]
Sending location checks: [10012610]
Sending location checks: [10012608]
Sending location checks: [10012610]
Sending location checks: [10012608]
Sending location checks: [10012601]
Sending location checks: [10012608]
Sending location checks: [10012614]
Sending location checks: [10012608]
Sending location checks: [10012607]
Sending location checks: [10002603]
Sending location checks: [10012608]
Sending location checks: [10012607]
Sending location checks: [10002603]
Sending location checks: [10012606]
Sending location checks: [10002603]
Sending location checks: [10012606]
Sending location checks: [10012605]
Sending location checks: [10010102]
Sending location checks: [10010202]
Sending location checks: [10010207]
Sending location checks: [10011501]
Sending location checks: [10011403]
Sending location checks: [10012705]
Sending location checks: [10012704]
Sending location checks: [10012704]
Sending location checks: [10012703]
Sending location checks: [10012609]
Sending location checks: [10002601]
Sending location checks: [10012611]
Sending location checks: [10012610]
Sending location checks: [10012608]
Sending location checks: [10012607]
Sending location checks: [10012606]
Sending location checks: [10012605]
Sending location checks: [10012612]
Sending location checks: [10002602]
Sending location checks: [10012613]
Sending location checks: [10012505]
Sending location checks: [10012613]
Sending location checks: [10012505]
Sending location checks: [10012613]
Sending location checks: [10012603]
Sending location checks: [10012613]
Sending location checks: [10012603]
Sending location checks: [10012507]
Sending location checks: [10012603]
Sending location checks: [10012508]
Sending location checks: [10012507]
Sending location checks: [10012508]
Sending location checks: [10012507]
Sending location checks: [10012614]
Sending location checks: [10012601]
Sending location checks: [10012614]
Sending location checks: [10012607]
Sending location checks: [10002603]
Sending location checks: [10012614]
Sending location checks: [10012507]
Sending location checks: [10012508]
Sending location checks: [10012506]
Sending location checks: [10012403]
Sending location checks: [10012506]
Sending location checks: [10012508]
Sending location checks: [10012506]
Sending location checks: [10012403]
Sending location checks: [10012404]
Sending location checks: [10012408]
Sending location checks: [10012914]
Sending location checks: [10012913]
Sending location checks: [10012911]
Sending location checks: [10012904]
Sending location checks: [10002901]
Sending location checks: [10012904]
Sending location checks: [10012909]
Sending location checks: [10012910]
Sending location checks: [10012909]
Sending location checks: [10012910]
Sending location checks: [10012912]
Sending location checks: [10012913]
Sending location checks: [10012914]
Sending location checks: [10012408]
Sending location checks: [10012404]
Sending location checks: [10001301]
Sending location checks: [10011301]
Sending location checks: [10011501]
Sending location checks: [10011403]
Sending location checks: [10011504]
Sending location checks: [10011703]
Sending location checks: [10011603]
Sending location checks: [10012801]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010504]
Sending location checks: [10010501]
Sending location checks: [10010504]
Sending location checks: [10010501]
Sending location checks: [10010505]
Sending location checks: [10010501]
Sending location checks: [10010505]
Sending location checks: [10011804]
Sending location checks: [10010505]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011804]
Sending location checks: [10011806]
Sending location checks: [10011805]
Sending location checks: [10010505]
Sending location checks: [10010501]
Sending location checks: [10000501]
Sending location checks: [10010501]
Sending location checks: [10010505]
Sending location checks: [10011804]
Sending location checks: [10011805]
Sending location checks: [10011807]
Sending location checks: [10011807]
Sending location checks: [10010701]
Sending location checks: [10011811]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010603]
Sending location checks: [10010604]
Sending location checks: [10010808]
Sending location checks: [10010604]
Sending location checks: [10010808]
Sending location checks: [10010806]
Sending location checks: [10010807]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010903]
Sending location checks: [10010905]
Sending location checks: [10010903]
Sending location checks: [10010901]
Sending location checks: [10010902]
Sending location checks: [10011003]
Sending location checks: [10011102]
Sending location checks: [10011103]
Sending location checks: [10011102]
Sending location checks: [10011103]
Sending location checks: [10011106]
Sending location checks: [10011107]
Sending location checks: [10011901]
Sending location checks: [10011003]
Sending location checks: [10012009]
Sending location checks: [10012010]
Sending location checks: [10012008]
Sending location checks: [10012110]
Sending location checks: [10012102]
Sending location checks: [10012103]
Sending location checks: [10012102]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012104]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012102]
Sending location checks: [10012103]
Sending location checks: [10012102]
Sending location checks: [10012110]
Sending location checks: [10012109]
Sending location checks: [10012110]
Sending location checks: [10012008]
Sending location checks: [10012010]
Sending location checks: [10012009]
Sending location checks: [10012010]
Sending location checks: [10012009]
Sending location checks: [10011003]
Sending location checks: [10012009]
Sending location checks: [10011901]
Sending location checks: [10010908]
Sending location checks: [10011901]
Sending location checks: [10010907]
Sending location checks: [10010908]
Sending location checks: [10010907]
Sending location checks: [10010910]
Sending location checks: [10010907]
Sending location checks: [10010908]
Sending location checks: [10011901]
Sending location checks: [10011003]
Sending location checks: [10011901]
Sending location checks: [10011003]
Sending location checks: [10011102]
Sending location checks: [10011103]
Sending location checks: [10010303]
Sending location checks: [10010303]
Sending location checks: [10010303]
Sending location checks: [10011108]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10001101]
Sending location checks: [10011108]
Sending location checks: [10010308]
Sending location checks: [10011108]
Sending location checks: [10010308]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10011205]
Sending location checks: [10011101]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10011108]
Sending location checks: [10012304]
Sending location checks: [10012404]
Sending location checks: [10012304]
Sending location checks: [10012404]
Sending location checks: [10012403]
Sending location checks: [10012404]
Sending location checks: [10012403]
Sending location checks: [10012506]
Sending location checks: [10012403]
Sending location checks: [10012506]
Sending location checks: [10012508]
Sending location checks: [10012506]
Sending location checks: [10012508]
Sending location checks: [10012507]
Sending location checks: [10012507]
Sending location checks: [10012508]
Sending location checks: [10012507]
Sending location checks: [10012604]
Sending location checks: [10012507]
Sending location checks: [10012603]
Sending location checks: [10012507]
Sending location checks: [10012406]
Sending location checks: [10012601]
Sending location checks: [10012406]
Sending location checks: [10012602]
Sending location checks: [10012610]
Sending location checks: [10012611]
Sending location checks: [10012609]
Sending location checks: [10002601]
Sending location checks: [10012703]
Sending location checks: [10012705]
Sending location checks: [10011403]
Sending location checks: [10012705]
Sending location checks: [10011403]
Sending location checks: [10011504]
Sending location checks: [10011703]
Sending location checks: [10011504]
Sending location checks: [10011703]
Sending location checks: [10011603]
Sending location checks: [10011703]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10010207]
Sending location checks: [10010104]
Sending location checks: [10010207]
Sending location checks: [10010104]
Sending location checks: [10010404]
Sending location checks: [10010404]
Sending location checks: [10000401]
Sending location checks: [10010404]
Sending location checks: [10010502]
Sending location checks: [10010404]
Sending location checks: [10010502]
Sending location checks: [10010503]
Sending location checks: [10010504]
Sending location checks: [10012812]
Sending location checks: [10012802]
Sending location checks: [10012812]
Sending location checks: [10012802]
Sending location checks: [10012812]
Sending location checks: [10010502]
Sending location checks: [10010404]
Sending location checks: [10000401]
Sending location checks: [10010404]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010104]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010207]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010103]
Sending location checks: [10010106]
"""


log_data_all_vanilla = [log_data_vanilla_1, log_data_vanilla_2, log_data_vanilla_3,
"""
Sending location checks: [10010805]
Sending location checks: [10011801]
""",
"""
Sending location checks: [10013013]
Sending location checks: [10013012]
Sending location checks: [10013013]
""",
"""
Sending location checks: [10012913]
Sending location checks: [10012917]
Sending location checks: [10012916]
Sending location checks: [10012905]
Sending location checks: [10012908]
"""
]

all_locations = [
10010101,
10010102,
10010103,
10010104,
10010105,
10010106,
10010107,
10010201,
10010202,
10010203,
10010204,
10010205,
10010206,
10010207,
10010301,
10010302,
10010303,
10010304,
10010305,
10010306,
10010307,
10010308,
10010309,
10010401,
10010402,
10010403,
10010404,
10010405,
10010406,
10010407,
10010408,
10010409,
10010501,
10010502,
10010503,
10010504,
10010505,
10010506,
10010601,
10010602,
10010603,
10010604,
10010605,
10010701,
10010702,
10010703,
10010704,
10010801,
10010802,
10010803,
10010804,
10010805,
10010806,
10010807,
10010808,
10010809,
10010810,
10010811,
10010901,
10010902,
10010903,
10010904,
10010905,
10010906,
10010907,
10010908,
10010909,
10010910,
10011001,
10011002,
10011003,
10011004,
10011005,
10011006,
10011007,
10011008,
10011009,
10011101,
10011102,
10011103,
10011104,
10011105,
10011106,
10011107,
10011108,
10011201,
10011202,
10011203,
10011204,
10011205,
10011301,
10011302,
10011303,
10011304,
10011401,
10011402,
10011403,
10011501,
10011502,
10011503,
10011504,
10011601,
10011602,
10011603,
10011701,
10011702,
10011703,
10011704,
10011801,
10011802,
10011803,
10011804,
10011805,
10011806,
10011807,
10011808,
10011809,
10011810,
10011811,
10011901,
10011902,
10011903,
10011904,
10011905,
10012001,
10012002,
10012003,
10012004,
10012005,
10012006,
10012007,
10012008,
10012009,
10012010,
10012101,
10012102,
10012103,
10012104,
10012105,
10012106,
10012107,
10012108,
10012109,
10012110,
10012111,
10012112,
10012113,
10012114,
10012115,
10012201,
10012202,
10012301,
10012302,
10012303,
10012304,
10012401,
10012402,
10012403,
10012404,
10012405,
10012406,
10012407,
10012408,
10012501,
10012502,
10012503,
10012504,
10012505,
10012506,
10012507,
10012508,
10012601,
10012602,
10012603,
10012604,
10012605,
10012606,
10012607,
10012608,
10012609,
10012610,
10012611,
10012612,
10012613,
10012614,
10012701,
10012702,
10012703,
10012704,
10012705,
10012706,
10012707,
10012708,
10012801,
10012802,
10012803,
10012804,
10012805,
10012806,
10012807,
10012808,
10012809,
10012810,
10012811,
10012812,
10012813,
10012814,
10012815,
10012816,
10012817,
10012818,
10012819,
10012820,
10012901,
10012902,
10012903,
10012904,
10012905,
10012906,
10012907,
10012908,
10012909,
10012910,
10012911,
10012912,
10012913,
10012914,
10012915,
10012916,
10012917,
10012918,
10013001,
10013002,
10013003,
10013004,
10013005,
10013006,
10013007,
10013008,
10013009,
10013010,
10013011,
10013012,
10013013,
10013014,
]


def create_all_pairs_from_logs(logs):
    data = []
    entries = []
    # accept either a single log string or an iterable of log strings
    if isinstance(logs, str):
        log_iter = [logs]
    else:
        log_iter = logs

    for log_data in log_iter:
        prev = None
        for line in log_data.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("Sending location checks:"):
                try:
                    location_id = int(line.split("[", 1)[1].split("]", 1)[0])
                except Exception:
                    continue
                if location_id <= 10010000:
                    continue
                entries += [location_id]
    entries = list(set(entries))
    for i in range(len(entries)):
        for j in range(len(entries)):
            if i != j:
                data.append((entries[i], entries[j]))
    data = list(set(data))
    return data

def create_connections_from_logs(logs):
    data = []
    # accept either a single log string or an iterable of log strings
    if isinstance(logs, str):
        log_iter = [logs]
    else:
        log_iter = logs

    for log_data in log_iter:
        prev = None
        for line in log_data.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("Sending location checks:"):
                try:
                    location_id = int(line.split("[", 1)[1].split("]", 1)[0])
                except Exception:
                    continue
                if location_id <= 10010000:
                    continue
                # Here you can process the location_id as needed
                if prev is not None:
                    if prev != location_id:
                        data.append((prev, location_id))
                prev = location_id
    data = list(set(data))
    return data
 
data = create_connections_from_logs(log_data_all_vanilla)

# create clusters:
# Build edges/nodes as ints
edges = [(int(a), int(b)) for a, b in data]
nodes = set()
for a, b in edges:
    nodes.add(a)
    nodes.add(b)

# adjacency (full directed graph)
adj = {n: set() for n in nodes}
for a, b in edges:
    adj.setdefault(a, set()).add(b)

# group nodes by (number - 10000)//100
groups = {}
for n in nodes:
    gid = (n - 10000) // 100
    groups.setdefault(gid, set()).add(n)

# Tarjan's algorithm to find SCCs within a given node subset
def tarjan_scc(node_subset):
    index = 0
    indices = {}
    lowlink = {}
    stack = []
    onstack = set()
    sccs = []

    def strong(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        onstack.add(v)

        for w in adj.get(v, ()):
            if w not in node_subset:
                continue  # only consider edges inside the subset
            if w not in indices:
                strong(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in onstack:
                lowlink[v] = min(lowlink[v], indices[w])

        if lowlink[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                onstack.remove(w)
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)

    for v in list(node_subset):
        if v not in indices:
            strong(v)
    return sccs

# Build clusters: for each group, find SCCs restricted to that group's nodes.
# Use the minimal number in the SCC as the cluster key.
clusters = {}
for gid, node_set in groups.items():
    sccs = tarjan_scc(node_set)
    for scc in sccs:
        if not scc:
            continue
        key = min(scc)
        clusters[key] = sorted(scc)

# collect already clustered nodes
clustered_nodes = set()
for nodes_list in clusters.values():
    clustered_nodes.update(nodes_list)

# ensure every node seen in edges is clustered (fallback singletons)
for n in nodes:
    if n not in clustered_nodes:
        clusters[n] = [n]
        clustered_nodes.add(n)

# ensure every location from all_locations is in some cluster (singleton if necessary)
for loc in all_locations:
    if loc not in clustered_nodes:
        clusters[loc] = [loc]
        clustered_nodes.add(loc)
        
#########################################################################################

log_data_jumppads = [
"""
Sending location checks: [10012810]
Sending location checks: [10012808]
""",
"""
Sending location checks: [10012704]
Sending location checks: [10012701]
""",
"""
Sending location checks: [10010202]
Sending location checks: [10010304]
Sending location checks: [10011005]
Sending location checks: [10010309]
Sending location checks: [10011005]
Sending location checks: [10010102]
Sending location checks: [10010202]
Sending location checks: [10010304]
Sending location checks: [10011104]
Sending location checks: [10011107]
Sending location checks: [10011001]
Sending location checks: [10001001]
Sending location checks: [10011001]
Sending location checks: [10011009]
Sending location checks: [10011009]
Sending location checks: [10010807]
Sending location checks: [10010604]
Sending location checks: [10010602]
Sending location checks: [10010107]
Sending location checks: [10010101]
Sending location checks: [10000101]
Sending location checks: [10010101]
Sending location checks: [10010201]
Sending location checks: [10010307]
Sending location checks: [10010306]
Sending location checks: [10011108]
Sending location checks: [10012304]
Sending location checks: [10012404]
Sending location checks: [10012403]
Sending location checks: [10012402]
Sending location checks: [10012409]
Sending location checks: [10012405]
Sending location checks: [10012401]
Sending location checks: [10012504]
Sending location checks: [10012707]
Sending location checks: [10012405]
Sending location checks: [10012405]
Sending location checks: [10012502]
Sending location checks: [10012401]
Sending location checks: [10012504]
Sending location checks: [10012501]
Sending location checks: [10012901]
Sending location checks: [10012902]
Sending location checks: [10012901]
Sending location checks: [10012901]
Sending location checks: [10012603]
Sending location checks: [10012508]
Sending location checks: [10012508]
Sending location checks: [10012506]
Sending location checks: [10012403]
Sending location checks: [10011401]
Sending location checks: [10011301]
Sending location checks: [10001301]
Sending location checks: [10011301]
Sending location checks: [10012409]
Sending location checks: [10012405]
Sending location checks: [10002401]
Sending location checks: [10012504]
Sending location checks: [10012501]
Sending location checks: [10012902]
Sending location checks: [10012507]
Sending location checks: [10012501]
Sending location checks: [10012504]
Sending location checks: [10012501]
Sending location checks: [10012502]
"""]

log_data_ledge_grab = [
"""
Sending location checks: [10012303]
Sending location checks: [10012301]
Sending location checks: [10012302]
""",
"""
Sending location checks: [10011701]
Sending location checks: [10011702]
""",
"""
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010107]
Sending location checks: [10010106]
Sending location checks: [10010107]
Sending location checks: [10010101]
Sending location checks: [10010107]
Sending location checks: [10010101]
Sending location checks: [10010104]
Sending location checks: [10010207]
Sending location checks: [10010206]
Sending location checks: [10010207]
Sending location checks: [10010206]
Sending location checks: [10010307]
Sending location checks: [10010206]
Sending location checks: [10010201]
Sending location checks: [10010206]
Sending location checks: [10010201]
Sending location checks: [10010101]
Sending location checks: [10000101]
Sending location checks: [10010101]
Sending location checks: [10010201]
Sending location checks: [10010202]
Sending location checks: [10010303]
Sending location checks: [10010304]
Sending location checks: [10010303]
Sending location checks: [10010304]
Sending location checks: [10010305]
Sending location checks: [10010304]
Sending location checks: [10010305]
Sending location checks: [10010301]
Sending location checks: [10010305]
Sending location checks: [10010301]
Sending location checks: [10010302]
Sending location checks: [10000301]
Sending location checks: [10010302]
Sending location checks: [10010301]
Sending location checks: [10010302]
Sending location checks: [10011203]
Sending location checks: [10010302]
Sending location checks: [10011202]
Sending location checks: [10010302]
Sending location checks: [10011202]
Sending location checks: [10012201]
Sending location checks: [10013006]
Sending location checks: [10013014]
Sending location checks: [10012910]
Sending location checks: [10013014]
Sending location checks: [10012910]
Sending location checks: [10012912]
Sending location checks: [10012911]
Sending location checks: [10012913]
Sending location checks: [10012914]
Sending location checks: [10012408]
Sending location checks: [10012408]
Sending location checks: [10012404]
Sending location checks: [10011401]
Sending location checks: [10012409]
Sending location checks: [10011401]
Sending location checks: [10012403]
Sending location checks: [10012409]
Sending location checks: [10012403]
Sending location checks: [10012409]
Sending location checks: [10012405]
Sending location checks: [10012405]
Sending location checks: [10012409]
Sending location checks: [10012402]
Sending location checks: [10012503]
Sending location checks: [10012402]
Sending location checks: [10012503]
Sending location checks: [10012506]
Sending location checks: [10012506]
Sending location checks: [10012508]
Sending location checks: [10012507]
Sending location checks: [10012507]
Sending location checks: [10012601]
Sending location checks: [10012406]
Sending location checks: [10012402]
Sending location checks: [10012405]
Sending location checks: [10012402]
Sending location checks: [10012405]
Sending location checks: [10012405]
Sending location checks: [10012702]
Sending location checks: [10010102]
Sending location checks: [10010303]
Sending location checks: [10010304]
Sending location checks: [10010305]
Sending location checks: [10010301]
Sending location checks: [10010306]
Sending location checks: [10010307]
Sending location checks: [10010201]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10010401]
Sending location checks: [10010402]
Sending location checks: [10010401]
Sending location checks: [10010402]
Sending location checks: [10010401]
Sending location checks: [10010405]
Sending location checks: [10010409]
Sending location checks: [10010403]
Sending location checks: [10010401]
Sending location checks: [10010204]
Sending location checks: [10010203]
Sending location checks: [10010204]
Sending location checks: [10010408]
Sending location checks: [10011603]
Sending location checks: [10010408]
Sending location checks: [10010205]
Sending location checks: [10010408]
Sending location checks: [10011603]
Sending location checks: [10010205]
Sending location checks: [10010204]
Sending location checks: [10010205]
Sending location checks: [10010204]
Sending location checks: [10010203]
Sending location checks: [10010204]
Sending location checks: [10010401]
Sending location checks: [10010204]
Sending location checks: [10010401]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10010401]
Sending location checks: [10010502]
Sending location checks: [10010501]
Sending location checks: [10010504]
Sending location checks: [10012812]
Sending location checks: [10012802]
Sending location checks: [10012820]
Sending location checks: [10012802]
Sending location checks: [10012814]
Sending location checks: [10012802]
Sending location checks: [10012814]
Sending location checks: [10012809]
Sending location checks: [10012811]
Sending location checks: [10012809]
Sending location checks: [10012811]
Sending location checks: [10012809]
Sending location checks: [10012814]
Sending location checks: [10012810]
Sending location checks: [10012814]
Sending location checks: [10012803]
Sending location checks: [10012814]
Sending location checks: [10012803]
Sending location checks: [10012818]
Sending location checks: [10002802]
Sending location checks: [10012803]
Sending location checks: [10012805]
Sending location checks: [10010102]
Sending location checks: [10010202]
Sending location checks: [10010207]
Sending location checks: [10010206]
Sending location checks: [10010207]
Sending location checks: [10010206]
Sending location checks: [10010207]
Sending location checks: [10010205]
Sending location checks: [10011703]
Sending location checks: [10011504]
Sending location checks: [10011403]
Sending location checks: [10001401]
Sending location checks: [10011403]
Sending location checks: [10012705]
Sending location checks: [10012702]
Sending location checks: [10012707]
Sending location checks: [10012702]
Sending location checks: [10012707]
Sending location checks: [10012702]
Sending location checks: [10012705]
Sending location checks: [10011403]
Sending location checks: [10001401]
Sending location checks: [10011504]
Sending location checks: [10011703]
Sending location checks: [10011603]
Sending location checks: [10010408]
Sending location checks: [10010406]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010501]
Sending location checks: [10000501]
Sending location checks: [10012813]
Sending location checks: [10010501]
Sending location checks: [10000501]
Sending location checks: [10010501]
Sending location checks: [10010505]
Sending location checks: [10010501]
Sending location checks: [10000501]
Sending location checks: [10010501]
Sending location checks: [10010505]
Sending location checks: [10010506]
Sending location checks: [10010407]
Sending location checks: [10010605]
Sending location checks: [10010603]
Sending location checks: [10010808]
Sending location checks: [10010603]
Sending location checks: [10010802]
Sending location checks: [10010801]
Sending location checks: [10010805]
Sending location checks: [10010801]
Sending location checks: [10010809]
Sending location checks: [10010801]
Sending location checks: [10010802]
Sending location checks: [10010802]
Sending location checks: [10010801]
Sending location checks: [10010809]
Sending location checks: [10010811]
Sending location checks: [10000801]
Sending location checks: [10010811]
Sending location checks: [10010604]
Sending location checks: [10010402]
Sending location checks: [10010401]
Sending location checks: [10000201]
Sending location checks: [10010201]
Sending location checks: [10010307]
Sending location checks: [10010306]
Sending location checks: [10010308]
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10011204]
Sending location checks: [10011205]
Sending location checks: [10011204]
Sending location checks: [10011202]
Sending location checks: [10011204]
Sending location checks: [10011202]
Sending location checks: [10011203]
Sending location checks: [10010302]
Sending location checks: [10011202]
Sending location checks: [10013007]
Sending location checks: [10013005]
Sending location checks: [10013004]
Sending location checks: [10013011]
Sending location checks: [10013004]
Sending location checks: [10012001]
Sending location checks: [10012001]
Sending location checks: [10012006]
Sending location checks: [10013010]
Sending location checks: [10012006]
Sending location checks: [10013010]
Sending location checks: [10012002]
Sending location checks: [10013010]
Sending location checks: [10012002]
Sending location checks: [10012003]
Sending location checks: [10012007]
Sending location checks: [10012003]
Sending location checks: [10012115]
Sending location checks: [10012003]
Sending location checks: [10012115]
Sending location checks: [10012111]
Sending location checks: [10012115]
Sending location checks: [10012111]
Sending location checks: [10012112]
Sending location checks: [10012111]
Sending location checks: [10012112]
Sending location checks: [10012105]
Sending location checks: [10012112]
Sending location checks: [10012112]
Sending location checks: [10012107]
Sending location checks: [10012112]
Sending location checks: [10012107]
Sending location checks: [10012113]
Sending location checks: [10011904]
Sending location checks: [10012114]
Sending location checks: [10011904]
Sending location checks: [10012114]
Sending location checks: [10012108]
Sending location checks: [10012104]
Sending location checks: [10012108]
Sending location checks: [10012104]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
PrintJSON message
Archipelago ServerMessage::PrintJSON: Goal { data: [Text { text: "Player1 (Team #1) has completed their goal." }], team: 0, slot: 1 }
PrintJSON message
Archipelago ServerMessage::PrintJSON: Collect { data: [Text { text: "Player1 (Team #1) has collected their items from other worlds." }], team: 0, slot: 1 }
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: None, players: None, checked_locations: Some([10010102, 10010103, 10010104, 10010105, 10010106, 10010107, 10010201, 10010202, 10010204, 10010205, 10010206, 10010207, 10010301, 10010303, 10010304, 10010305, 10010306, 10010307, 10010308, 10010309, 10010401, 10010402, 10010403, 10010405, 10010406, 10010407, 10010408, 10010409, 10010502, 10010503, 10010504, 10010505, 10010506, 10010602, 10010603, 10010604, 10010605, 10010703, 10010704, 10010801, 10010802, 10010803, 10010804, 10010805, 10010806, 10010807, 10010808, 10010809, 10010901, 10010902, 10010903, 10010904, 10010905, 10010907, 10010908, 10010909, 10010910, 10011002, 10011004, 10011005, 10011006, 10011007, 10011008, 10011009, 10011101, 10011102, 10011103, 10011104, 10011105, 10011106, 10011107, 10011202, 10011203, 10011204, 10011205, 10011302, 10011303, 10011304, 10011401, 10011402, 10011501, 10011503, 10011504, 10011602, 10011603, 10011701, 10011703, 10011704, 10011803, 10011804, 10011805, 10011806, 10011807, 10011808, 10011809, 10011810, 10011811, 10011901, 10011902, 10011903, 10011904, 10012001, 10012002, 10012003, 10012004, 10012005, 10012006, 10012008, 10012009, 10012010, 10012101, 10012102, 10012103, 10012104, 10012105, 10012106, 10012107, 10012109, 10012110, 10012111, 10012112, 10012113, 10012114, 10012115, 10012201, 10012301, 10012302, 10012304, 10012402, 10012403, 10012404, 10012405, 10012406, 10012407, 10012408, 10012501, 10012502, 10012503, 10012504, 10012506, 10012507, 10012508, 10012601, 10012602, 10012603, 10012604, 10012605, 10012606, 10012608, 10012610, 10012611, 10012613, 10012614, 10012701, 10012702, 10012703, 10012704, 10012705, 10012706, 10012707, 10012801, 10012802, 10012803, 10012804, 10012805, 10012806, 10012807, 10012809, 10012810, 10012811, 10012812, 10012814, 10012815, 10012816, 10012817, 10012819, 10012820, 10012901, 10012902, 10012903, 10012905, 10012906, 10012907, 10012908, 10012909, 10012910, 10012911, 10012912, 10012913, 10012914, 10012915, 10012916, 10012917, 10012918, 10013001, 10013002, 10013003, 10013004, 10013005, 10013006, 10013007, 10013008, 10013009, 10013010, 10013011, 10013013, 10013014]), missing_locations: None }
PrintJSON message
Archipelago ServerMessage::PrintJSON: Release { data: [Text { text: "Player1 (Team #1) has released all remaining items from their world." }], team: 0, slot: 1 }
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: None, players: None, checked_locations: Some([10010102, 10010103, 10010104, 10010105, 10010106, 10010107, 10010201, 10010202, 10010204, 10010205, 10010206, 10010207, 10010301, 10010303, 10010304, 10010305, 10010306, 10010307, 10010308, 10010309, 10010401, 10010402, 10010403, 10010405, 10010406, 10010407, 10010408, 10010409, 10010502, 10010503, 10010504, 10010505, 10010506, 10010602, 10010603, 10010604, 10010605, 10010703, 10010704, 10010801, 10010802, 10010803, 10010804, 10010805, 10010806, 10010807, 10010808, 10010809, 10010901, 10010902, 10010903, 10010904, 10010905, 10010907, 10010908, 10010909, 10010910, 10011002, 10011004, 10011005, 10011006, 10011007, 10011008, 10011009, 10011101, 10011102, 10011103, 10011104, 10011105, 10011106, 10011107, 10011202, 10011203, 10011204, 10011205, 10011302, 10011303, 10011304, 10011401, 10011402, 10011501, 10011503, 10011504, 10011602, 10011603, 10011701, 10011703, 10011704, 10011803, 10011804, 10011805, 10011806, 10011807, 10011808, 10011809, 10011810, 10011811, 10011901, 10011902, 10011903, 10011904, 10012001, 10012002, 10012003, 10012004, 10012005, 10012006, 10012008, 10012009, 10012010, 10012101, 10012102, 10012103, 10012104, 10012105, 10012106, 10012107, 10012109, 10012110, 10012111, 10012112, 10012113, 10012114, 10012115, 10012201, 10012301, 10012302, 10012304, 10012402, 10012403, 10012404, 10012405, 10012406, 10012407, 10012408, 10012501, 10012502, 10012503, 10012504, 10012506, 10012507, 10012508, 10012601, 10012602, 10012603, 10012604, 10012605, 10012606, 10012608, 10012610, 10012611, 10012613, 10012614, 10012701, 10012702, 10012703, 10012704, 10012705, 10012706, 10012707, 10012801, 10012802, 10012803, 10012804, 10012805, 10012806, 10012807, 10012809, 10012810, 10012811, 10012812, 10012814, 10012815, 10012816, 10012817, 10012819, 10012820, 10012901, 10012902, 10012903, 10012905, 10012906, 10012907, 10012908, 10012909, 10012910, 10012911, 10012912, 10012913, 10012914, 10012915, 10012916, 10012917, 10012918, 10013001, 10013002, 10013003, 10013004, 10013005, 10013006, 10013007, 10013008, 10013009, 10013010, 10013011, 10013013, 10013014]), missing_locations: None }
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Team #1 has completed all of their games! Congratulations!" }] }
Sending location checks: [10012104]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012106]
Sending location checks: [10012104]
Sending location checks: [10012106]
Archipelago: goal!
Sending location checks: [10012101]
Sending status update: ClientGoal
Sending location checks: [10012102]
Sending location checks: [10012110]
Sending location checks: [10012010]
Sending location checks: [10012009]
Sending location checks: [10011003]
Sending location checks: [10001002]
Sending location checks: [10011003]
Sending location checks: [10011107]
Sending location checks: [10011106]
Sending location checks: [10010309]
Sending location checks: [10011106]
Sending location checks: [10011104]
Sending location checks: [10010309]
Sending location checks: [10011104]
Sending location checks: [10011005]
Sending location checks: [10011104]
Sending location checks: [10010303]
Sending location checks: [10011005]
Sending location checks: [10010303]
Sending location checks: [10010102]
Sending location checks: [10011005]
Sending location checks: [10010102]
Sending location checks: [10011005]
Sending location checks: [10011005]
Sending location checks: [10011007]
Sending location checks: [10011005]
Sending location checks: [10011007]
Sending location checks: [10011006]
Sending location checks: [10011008]
Sending location checks: [10011008]
Sending location checks: [10011004]
Sending location checks: [10011004]
Sending location checks: [10010807]
Sending location checks: [10010806]
Sending location checks: [10010803]
Sending location checks: [10010805]
Sending location checks: [10010811]
Sending location checks: [10010810]
Sending location checks: [10010402]
Sending location checks: [10010401]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10010401]
Sending location checks: [10010502]
Sending location checks: [10010503]
Sending location checks: [10010504]
Sending location checks: [10012812]
Sending location checks: [10012802]
Sending location checks: [10012820]
Sending location checks: [10012804]
Sending location checks: [10012820]
Sending location checks: [10011602]
Sending location checks: [10012820]
Sending location checks: [10011602]
Sending location checks: [10012804]
Sending location checks: [10012807]
Sending location checks: [10012804]
Sending location checks: [10012807]
Sending location checks: [10011601]
Sending location checks: [10001601]
Sending location checks: [10011601]
Sending location checks: [10011602]
Sending location checks: [10011601]
Sending location checks: [10011602]
Sending location checks: [10011601]
Sending location checks: [10011602]
Sending location checks: [10012804]
Sending location checks: [10012807]
Sending location checks: [10012806]
Sending location checks: [10011601]
Sending location checks: [10012806]
Sending location checks: [10011601]
Sending location checks: [10001601]
Sending location checks: [10011601]
Sending location checks: [10011701]
Sending location checks: [10011601]
Sending location checks: [10011701]
Sending location checks: [10011704]
Sending location checks: [10011701]
Sending location checks: [10011503]
Sending location checks: [10011701]
Sending location checks: [10001701]
Sending location checks: [10011701]
Sending location checks: [10011704]
Sending location checks: [10012708]
Sending location checks: [10002701]
Sending location checks: [10012708]
Sending location checks: [10011402]
Sending location checks: [10012708]
Sending location checks: [10002701]
Sending location checks: [10012708]
Sending location checks: [10002701]
Sending location checks: [10012708]
Sending location checks: [10011402]
Sending location checks: [10012708]
Sending location checks: [10002701]
Sending location checks: [10012708]
Sending location checks: [10011704]
Sending location checks: [10011701]
Sending location checks: [10011503]
Sending location checks: [10001501]
Sending location checks: [10011502]
Sending location checks: [10011302]
Sending location checks: [10011502]
Sending location checks: [10011302]
Sending location checks: [10011304]
Sending location checks: [10011302]
Sending location checks: [10011303]
Sending location checks: [10011304]
Sending location checks: [10011303]
Sending location checks: [10011304]
Sending location checks: [10011302]
Sending location checks: [10011301]
Sending location checks: [10012409]
Sending location checks: [10012503]
Sending location checks: [10012502]
Sending location checks: [10012504]
Sending location checks: [10012502]
Sending location checks: [10012504]
Sending location checks: [10012501]
Sending location checks: [10012504]
Sending location checks: [10012501]
Sending location checks: [10012503]
Sending location checks: [10012403]
Sending location checks: [10011401]
Sending location checks: [10012404]
Sending location checks: [10012408]
Sending location checks: [10012408]
Sending location checks: [10012404]
Sending location checks: [10001301]
Sending location checks: [10011301]
Sending location checks: [10012409]
Sending location checks: [10012405]
Sending location checks: [10012405]
Sending location checks: [10012702]
Sending location checks: [10012705]
Sending location checks: [10011403]
Sending location checks: [10001401]
Sending location checks: [10011403]
Sending location checks: [10011501]
Sending location checks: [10011301]
Sending location checks: [10001301]
Sending location checks: [10011301]
Sending location checks: [10001301]
Sending location checks: [10011301]
Sending location checks: [10011401]
Sending location checks: [10012304]
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10011204]
Sending location checks: [10011205]
Sending location checks: [10011204]
Sending location checks: [10013007]
Sending location checks: [10011204]
Sending location checks: [10013007]
Sending location checks: [10013008]
Sending location checks: [10013007]
Sending location checks: [10010102]
Sending location checks: [10011005]
Sending location checks: [10011007]
Sending location checks: [10011008]
Sending location checks: [10011006]
Sending location checks: [10011901]
Sending location checks: [10011003]
Sending location checks: [10012009]
Sending location checks: [10012010]
Sending location checks: [10012005]
Sending location checks: [10012004]
Sending location checks: [10012005]
Sending location checks: [10012004]
Sending location checks: [10012003]
Sending location checks: [10012004]
Sending location checks: [10012003]
Sending location checks: [10012007]
Sending location checks: [10012003]
Sending location checks: [10012007]
Sending location checks: [10012007]
Sending location checks: [10002001]
Sending location checks: [10012007]
Sending location checks: [10002001]
Sending location checks: [10012007]
Sending location checks: [10002001]
Sending location checks: [10012007]
Sending location checks: [10002001]
Sending location checks: [10012007]
Sending location checks: [10002001]
Sending location checks: [10012007]
Sending location checks: [10012002]
Sending location checks: [10013011]
Sending location checks: [10013011]
Sending location checks: [10013004]
Sending location checks: [10013005]
Sending location checks: [10013008]
Sending location checks: [10013007]
Sending location checks: [10011204]
Sending location checks: [10011108]
Sending location checks: [10011108]
Sending location checks: [10010308]
Sending location checks: [10010306]
Sending location checks: [10010307]
Sending location checks: [10010201]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10010201]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10010401]
Sending location checks: [10010402]
Sending location checks: [10010401]
Sending location checks: [10010203]
Sending location checks: [10000201]
Sending location checks: [10010203]
Sending location checks: [10010201]
Sending location checks: [10010307]
Sending location checks: [10010306]
Sending location checks: [10010301]
Sending location checks: [10010302]
Sending location checks: [10000301]
Sending location checks: [10010302]
Sending location checks: [10000301]
Sending location checks: [10010301]
"""]

log_data_swim = ["""
Sending location checks: [10011802]
Sending location checks: [10010303]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10011504]
Sending location checks: [10012704]
Sending location checks: [10012704]
Sending location checks: [10012703]
Sending location checks: [10012611]
Sending location checks: [10012610]
Sending location checks: [10012608]
Sending location checks: [10012602]
Sending location checks: [10012406]
Sending location checks: [10012601]
Sending location checks: [10012614]
Sending location checks: [10012606]
Sending location checks: [10012605]
Sending location checks: [10012604]
Sending location checks: [10012507]
Sending location checks: [10012508]
Sending location checks: [10012603]
Sending location checks: [10012613]
Sending location checks: [10012906]
Sending location checks: [10012907]
Sending location checks: [10012906]
Sending location checks: [10012903]
Sending location checks: [10012915]
Sending location checks: [10012918]
Sending location checks: [10012903]
Sending location checks: [10012506]
Sending location checks: [10012403]
Sending location checks: [10011401]
Sending location checks: [10012706]
Sending location checks: [10011401]
Sending location checks: [10012404]
Sending location checks: [10012304]
Sending location checks: [10012404]
Sending location checks: [10012903]
Sending location checks: [10012915]
Sending location checks: [10012407]
Sending location checks: [10012201]
Sending location checks: [10013006]
Sending location checks: [10013014]
Sending location checks: [10013002]
Sending location checks: [10013001]
Sending location checks: [10012001]
Sending location checks: [10012109]
Sending location checks: [10012102]
Sending location checks: [10012106]
Sending location checks: [10012008]
Sending location checks: [10012108]
Sending location checks: [10011901]
Sending location checks: [10011902]
Sending location checks: [10010910]
Sending location checks: [10010909]
Sending location checks: [10010804]
Sending location checks: [10000702]
Sending location checks: [10010701]
Sending location checks: [10011811]
Sending location checks: [10011808]
Sending location checks: [10010506]
Sending location checks: [10010407]
Sending location checks: [10010605]
Sending location checks: [10010603]
Sending location checks: [10011811]
Sending location checks: [10010701]
Sending location checks: [10000701]
Sending location checks: [10010701]
Sending location checks: [10012816]
Sending location checks: [10012815]
Sending location checks: [10012819]
Sending location checks: [10012817]
Sending location checks: [10012801]
Sending location checks: [10010408]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10012801]
Sending location checks: [10012817]
Sending location checks: [10011703]
Sending location checks: [10012704]
Sending location checks: [10012704]
Sending location checks: [10012703]
Sending location checks: [10012611]
Sending location checks: [10012602]
Sending location checks: [10012601]
Sending location checks: [10012507]
Sending location checks: [10012507]
Sending location checks: [10012508]
Sending location checks: [10012915]
Sending location checks: [10012407]
Sending location checks: [10012201]
Sending location checks: [10013006]
Sending location checks: [10013014]
Sending location checks: [10013001]
Sending location checks: [10013003]
Sending location checks: [10011102]
Sending location checks: [10011105]
Sending location checks: [10011101]
Sending location checks: [10011105]
Sending location checks: [10011103]
Sending location checks: [10011106]
Sending location checks: [10011107]
Sending location checks: [10011104]
Sending location checks: [10011107]
Sending location checks: [10011901]
Sending location checks: [10010908]
Sending location checks: [10011901]
Sending location checks: [10011901]
Sending location checks: [10011107]
Sending location checks: [10011104]
Sending location checks: [10010303]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10012801]
Sending location checks: [10012815]
Sending location checks: [10012816]
Sending location checks: [10010506]
Sending location checks: [10010408]
Sending location checks: [10010406]
Sending location checks: [10010104]
Sending location checks: [10010104]
"""]
10011007
log_data_one_wall_jump = ["""
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 1, items: [NetworkItem { item: 10000002, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #2 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 2\" to Player1" }] }
Sending location checks: [10010105]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010105", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010105, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 2, items: [NetworkItem { item: 9999999, location: 10010105, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(2), players: None, checked_locations: Some([10010105]), missing_locations: None }
Sending location checks: [10010104]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "10000008", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010104", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 10000008, location: 10010104, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 3, items: [NetworkItem { item: 10000008, location: 10010104, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #8 in-game
Gonna activate all buttons
Gonna deactivate all buttons
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(3), players: None, checked_locations: Some([10010104]), missing_locations: None }
Sending location checks: [10010207]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010207", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010207, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 4, items: [NetworkItem { item: 9999999, location: 10010207, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(4), players: None, checked_locations: Some([10010207]), missing_locations: None }
Sending location checks: [10010202]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010202", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010202, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 5, items: [NetworkItem { item: 9999999, location: 10010202, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(5), players: None, checked_locations: Some([10010202]), missing_locations: None }
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10010207]
Sending location checks: [10010207]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 6, items: [NetworkItem { item: 9999991, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #-9 in-game
Archipelago: setting wall jump to 1
Archipelago: setting ledge grab to -1
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Progressive Wall Jump\" to Player1" }] }
Sending location checks: [10010206]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010206", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010206, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 7, items: [NetworkItem { item: 9999999, location: 10010206, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(6), players: None, checked_locations: Some([10010206]), missing_locations: None }
Sending location checks: [10010207]
Sending location checks: [10010206]
Sending location checks: [10010207]
Sending location checks: [10010205]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010205", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010205, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 8, items: [NetworkItem { item: 9999999, location: 10010205, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(7), players: None, checked_locations: Some([10010205]), missing_locations: None }
Sending location checks: [10010207]
Sending location checks: [10010104]
Sending location checks: [10010105]
Sending location checks: [10010105]
Sending location checks: [10010202]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010103", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010103, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 9, items: [NetworkItem { item: 9999999, location: 10010103, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(8), players: None, checked_locations: Some([10010103]), missing_locations: None }
Sending location checks: [10010106]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010106", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010106, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 10, items: [NetworkItem { item: 9999999, location: 10010106, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(9), players: None, checked_locations: Some([10010106]), missing_locations: None }
Sending location checks: [10010103]
Sending location checks: [10010104]
Sending location checks: [10010207]
New Game
Gonna deactivate all buttons
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 11, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010102]
Sending location checks: [10010303]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010303", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010303, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 12, items: [NetworkItem { item: 9999999, location: 10010303, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(10), players: None, checked_locations: Some([10010303]), missing_locations: None }
Sending location checks: [10010303]
Sending location checks: [10010303]
Sending location checks: [10010304]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010304", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010304, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 13, items: [NetworkItem { item: 9999999, location: 10010304, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(11), players: None, checked_locations: Some([10010304]), missing_locations: None }
Sending location checks: [10010303]
Sending location checks: [10010309]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010309", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010309, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 14, items: [NetworkItem { item: 9999999, location: 10010309, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(12), players: None, checked_locations: Some([10010309]), missing_locations: None }
Sending location checks: [10010304]
Sending location checks: [10010304]
Sending location checks: [10010303]
Sending location checks: [10010308]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010308", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010308, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 15, items: [NetworkItem { item: 9999999, location: 10010308, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(13), players: None, checked_locations: Some([10010308]), missing_locations: None }
Sending location checks: [10010306]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010306", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010306, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 16, items: [NetworkItem { item: 9999999, location: 10010306, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(14), players: None, checked_locations: Some([10010306]), missing_locations: None }
Sending location checks: [10010307]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010307", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010307, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 17, items: [NetworkItem { item: 9999999, location: 10010307, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(15), players: None, checked_locations: Some([10010307]), missing_locations: None }
Sending location checks: [10010306]
Sending location checks: [10010305]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010305", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010305, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 18, items: [NetworkItem { item: 9999999, location: 10010305, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(16), players: None, checked_locations: Some([10010305]), missing_locations: None }
Sending location checks: [10010306]
Sending location checks: [10010306]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 19, items: [NetworkItem { item: 10000004, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #4 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 4\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010408]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "10000016", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010408", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 10000016, location: 10010408, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 20, items: [NetworkItem { item: 10000016, location: 10010408, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #16 in-game
Gonna activate all buttons
Gonna deactivate all buttons
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(17), players: None, checked_locations: Some([10010408]), missing_locations: None }
Sending location checks: [10010406]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010406", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010406, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 21, items: [NetworkItem { item: 9999999, location: 10010406, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(18), players: None, checked_locations: Some([10010406]), missing_locations: None }
Sending location checks: [10010404]
Sending location checks: [10010407]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010407", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010407, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 22, items: [NetworkItem { item: 9999999, location: 10010407, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(19), players: None, checked_locations: Some([10010407]), missing_locations: None }
Sending location checks: [10010404]
Sending location checks: [10010406]
Sending location checks: [10010408]
Sending location checks: [10011603]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "10000013", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10011603", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 10000013, location: 10011603, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 23, items: [NetworkItem { item: 10000013, location: 10011603, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #13 in-game
Gonna activate all buttons
Gonna deactivate all buttons
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(20), players: None, checked_locations: Some([10011603]), missing_locations: None }
Sending location checks: [10011603]
Sending location checks: [10010408]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
New Game
Gonna deactivate all buttons
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 24, items: [NetworkItem { item: 10000005, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #5 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 5\" to Player1" }] }
Sending location checks: [10010105]
Sending location checks: [10010105]
Sending location checks: [10010104]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 25, items: [NetworkItem { item: 10000004, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #4 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 4\" to Player1" }] }
Sending location checks: [10010406]
Sending location checks: [10010506]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010506", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010506, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 26, items: [NetworkItem { item: 9999999, location: 10010506, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(21), players: None, checked_locations: Some([10010506]), missing_locations: None }
Sending location checks: [10010502]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "10000028", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010502", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 10000028, location: 10010502, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 27, items: [NetworkItem { item: 10000028, location: 10010502, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #28 in-game
Gonna activate all buttons
Gonna deactivate all buttons
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(22), players: None, checked_locations: Some([10010502]), missing_locations: None }
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 28, items: [NetworkItem { item: 10000004, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #4 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 4\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 29, items: [NetworkItem { item: 10000005, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #5 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 5\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010406]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010506]
Sending location checks: [10010502]
Sending location checks: [10010506]
Sending location checks: [10010502]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 30, items: [NetworkItem { item: 10000006, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #6 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 6\" to Player1" }] }
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 31, items: [NetworkItem { item: 10000006, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #6 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 6\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010106]
Sending location checks: [10010106]
Sending location checks: [10010605]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010605", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010605, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 32, items: [NetworkItem { item: 9999999, location: 10010605, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(23), players: None, checked_locations: Some([10010605]), missing_locations: None }
Sending location checks: [10010602]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010602", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010602, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 33, items: [NetworkItem { item: 9999999, location: 10010602, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(24), players: None, checked_locations: Some([10010602]), missing_locations: None }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 34, items: [NetworkItem { item: 10000007, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #7 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 7\" to Player1" }] }
Sending location checks: [10010601]
Sending location checks: [10000601]
Sending location checks: [10010601]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 35, items: [NetworkItem { item: 10000008, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #8 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 8\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 36, items: [NetworkItem { item: 10000009, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #9 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 9\" to Player1" }] }
Sending location checks: [10010808]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010808", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010808, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 37, items: [NetworkItem { item: 9999999, location: 10010808, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(25), players: None, checked_locations: Some([10010808]), missing_locations: None }
Sending location checks: [10010807]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010807", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010807, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 38, items: [NetworkItem { item: 9999999, location: 10010807, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(26), players: None, checked_locations: Some([10010807]), missing_locations: None }
Sending location checks: [10010806]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010806", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010806, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 39, items: [NetworkItem { item: 9999999, location: 10010806, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(27), players: None, checked_locations: Some([10010806]), missing_locations: None }
Sending location checks: [10010806]
Sending location checks: [10010905]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010905", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010905, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 40, items: [NetworkItem { item: 9999999, location: 10010905, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(28), players: None, checked_locations: Some([10010905]), missing_locations: None }
Sending location checks: [10010903]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "10000004", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010903", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 10000004, location: 10010903, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 41, items: [NetworkItem { item: 10000004, location: 10010903, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #4 in-game
Gonna activate all buttons
Gonna deactivate all buttons
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(29), players: None, checked_locations: Some([10010903]), missing_locations: None }
Sending location checks: [10010901]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "10000017", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010901", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 10000017, location: 10010901, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 42, items: [NetworkItem { item: 10000017, location: 10010901, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #17 in-game
Gonna activate all buttons
Gonna deactivate all buttons
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(30), players: None, checked_locations: Some([10010901]), missing_locations: None }
Sending location checks: [10010902]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010902", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010902, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 43, items: [NetworkItem { item: 9999999, location: 10010902, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(31), players: None, checked_locations: Some([10010902]), missing_locations: None }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 44, items: [NetworkItem { item: 10000010, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #10 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 10\" to Player1" }] }
Sending location checks: [10011004]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "10000012", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10011004", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 10000012, location: 10011004, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 45, items: [NetworkItem { item: 10000012, location: 10011004, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #12 in-game
Gonna activate all buttons
Gonna deactivate all buttons
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(32), players: None, checked_locations: Some([10011004]), missing_locations: None }
Sending location checks: [10011009]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10011009", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10011009, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 46, items: [NetworkItem { item: 9999999, location: 10011009, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(33), players: None, checked_locations: Some([10011009]), missing_locations: None }
Sending location checks: [10011001]
Sending location checks: [10001001]
Sending location checks: [10011001]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 47, items: [NetworkItem { item: 10000010, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #10 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 10\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 48, items: [NetworkItem { item: 10000009, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #9 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 9\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010102]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 49, items: [NetworkItem { item: 10000010, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #10 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 10\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010102]
Sending location checks: [10011005]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999991", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10011005", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999991, location: 10011005, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 50, items: [NetworkItem { item: 9999991, location: 10011005, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-9 in-game
Archipelago: setting wall jump to 2
Archipelago: setting ledge grab to -1
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(34), players: None, checked_locations: Some([10011005]), missing_locations: None }
New Game
Gonna deactivate all buttons
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 51, items: [NetworkItem { item: 10000010, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #10 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 10\" to Player1" }] }
Sending location checks: [10011005]
Sending location checks: [10010107]
PrintJSON message
Archipelago ServerMessage::PrintJSON: ItemSend { data: [PlayerId { text: "1" }, Text { text: " found their " }, ItemId { text: "9999999", flags: 1, player: 1 }, Text { text: " (" }, LocationId { text: "10010107", player: 1 }, Text { text: ")" }], receiving: 1, item: NetworkItem { item: 9999999, location: 10010107, player: 1, flags: 1 } }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 52, items: [NetworkItem { item: 9999999, location: 10010107, player: 1, flags: 1 }] }
APAPAP Trigger Cluster #-1 in-game
RoomUpdate message
Archipelago ServerMessage::RoomUpdate: RoomUpdate { version: None, tags: None, password_required: false, permissions: None, hint_cost: None, location_check_points: None, games: None, datapackage_versions: None, datapackage_checksums: None, seed_name: None, time: None, hint_points: Some(35), players: None, checked_locations: Some([10010107]), missing_locations: None }
Sending location checks: [10010101]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 53, items: [NetworkItem { item: 10000011, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #11 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 11\" to Player1" }] }
Sending location checks: [10010102]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 54, items: [NetworkItem { item: 10000012, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #12 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 12\" to Player1" }] }
Sending location checks: [10010102]
New Game
Gonna deactivate all buttons
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 55, items: [NetworkItem { item: 10000013, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #13 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 13\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 56, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
Sending location checks: [10010303]
Sending location checks: [10010303]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 57, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010303]
Sending location checks: [10010308]
Sending location checks: [10010303]
Sending location checks: [10010308]
Sending location checks: [10010306]
""",
"""
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 207, items: [NetworkItem { item: 60000005, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #50000005 in-game
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Disable Swim\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 208, items: [NetworkItem { item: 60000000, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #50000000 in-game
Archipelago: setting wall jump to 0
Archipelago: setting ledge grab to 0
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Disable Wall Ledge\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 209, items: [NetworkItem { item: 60000010, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #50000010 in-game
Archipelago: setting jump pads to 0
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Disable Jumppads\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 210, items: [NetworkItem { item: 60000001, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #50000001 in-game
Archipelago: setting wall jump to 1
Archipelago: setting ledge grab to -1
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Enable One Wall\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 211, items: [NetworkItem { item: 10000011, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #11 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 11\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 212, items: [NetworkItem { item: 10000012, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #12 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 12\" to Player1" }] }
Sending location checks: [10011104]
Sending location checks: [10011106]
Sending location checks: [10011103]
Sending location checks: [10011105]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10011108]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 213, items: [NetworkItem { item: 10000013, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #13 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 13\" to Player1" }] }
Sending location checks: [10001101]
Sending location checks: [10011108]
Sending location checks: [10011101]
Sending location checks: [10011105]
Sending location checks: [10011103]
Sending location checks: [10011106]
Sending location checks: [10011104]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 214, items: [NetworkItem { item: 10000014, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #14 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 14\" to Player1" }] }
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 215, items: [NetworkItem { item: 10000015, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #15 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 15\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010105]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 216, items: [NetworkItem { item: 10000016, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #16 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 16\" to Player1" }] }
Sending location checks: [10010104]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 217, items: [NetworkItem { item: 10000017, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #17 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 17\" to Player1" }] }
Sending location checks: [10010105]
Sending location checks: [10010104]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 218, items: [NetworkItem { item: 10000018, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #18 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 18\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 219, items: [NetworkItem { item: 10000006, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #6 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 6\" to Player1" }] }
Sending location checks: [10010605]
Sending location checks: [10000601]
Sending location checks: [10010601]
Sending location checks: [10011810]
Sending location checks: [10011805]
Sending location checks: [10011806]
Sending location checks: [10011805]
Sending location checks: [10011807]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010605]
Sending location checks: [10000601]
Sending location checks: [10010601]
Sending location checks: [10000601]
Sending location checks: [10010601]
Sending location checks: [10011810]
Sending location checks: [10011805]
Sending location checks: [10011806]
Sending location checks: [10011807]
Sending location checks: [10011805]
Sending location checks: [10011807]
Sending location checks: [10011811]
Sending location checks: [10011808]
Sending location checks: [10011811]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 220, items: [NetworkItem { item: 10000019, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #19 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 19\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 221, items: [NetworkItem { item: 10000010, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #10 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 10\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10010107]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10011005]
Sending location checks: [10010107]
""","""
Sending location checks: [10011007]
Sending location checks: [10011006]
Sending location checks: [10011004]
Sending location checks: [10011901]
Sending location checks: [10011902]
Sending location checks: [10011903]
Sending location checks: [10011904]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 222, items: [NetworkItem { item: 10000020, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #20 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 20\" to Player1" }] }
Sending location checks: [10011904]
Sending location checks: [10011903]
Sending location checks: [10011905]
Sending location checks: [10001901]
Sending location checks: [10011905]
Sending location checks: [10012009]
Sending location checks: [10012010]
Sending location checks: [10012005]
Sending location checks: [10012006]
Sending location checks: [10012005]
Sending location checks: [10012005]
Sending location checks: [10012006]
Sending location checks: [10012001]
Sending location checks: [10012006]
Sending location checks: [10012005]
Sending location checks: [10012005]
Sending location checks: [10012010]
Sending location checks: [10012008]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 223, items: [NetworkItem { item: 10000021, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #21 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 21\" to Player1" }] }
Sending location checks: [10012110]
Sending location checks: [10012008]
Sending location checks: [10012102]
Sending location checks: [10012101]
Sending location checks: [10012104]
Sending location checks: [10012108]
Sending location checks: [10011903]
Sending location checks: [10011903]
Sending location checks: [10011904]
""",
"""
Sending location checks: [10012915]
Sending location checks: [10012914]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 257, items: [NetworkItem { item: 10000030, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #30 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 30\" to Player1" }] }
New Game
Gonna deactivate all buttons
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 258, items: [NetworkItem { item: 10000030, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #30 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 30\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 259, items: [NetworkItem { item: 10000011, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #11 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 11\" to Player1" }] }
Sending location checks: [10011104]
Sending location checks: [10011106]
Sending location checks: [10011103]
Sending location checks: [10011102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 260, items: [NetworkItem { item: 10000012, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #12 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 12\" to Player1" }] }
Sending location checks: [10011105]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10013006]
Sending location checks: [10013013]
Sending location checks: [10013006]
Sending location checks: [10013013]
Sending location checks: [10013013]
Sending location checks: [10013006]
Sending location checks: [10013013]
Sending location checks: [10013002]
Sending location checks: [10013001]
Sending location checks: [10013001]
Sending location checks: [10013001]
Sending location checks: [10013001]
Sending location checks: [10013001]
Sending location checks: [10013003]
Sending location checks: [10013001]
Sending location checks: [10013002]
Sending location checks: [10013013]
Sending location checks: [10013006]
Sending location checks: [10013013]
Sending location checks: [10013013]
Sending location checks: [10013006]
Sending location checks: [10013013]
Sending location checks: [10013013]
Sending location checks: [10013013]
Sending location checks: [10013013]
""",
"""
Sending location checks: [10010102]
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 225, items: [NetworkItem { item: 10000020, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #20 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 20\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 226, items: [NetworkItem { item: 10000021, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #21 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 21\" to Player1" }] }
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 227, items: [NetworkItem { item: 10000010, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #10 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 10\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 228, items: [NetworkItem { item: 10000019, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #19 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 19\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 229, items: [NetworkItem { item: 10000021, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #21 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 21\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10011005]
Sending location checks: [10010102]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10010102]
Sending location checks: [10010102]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10010107]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10011005]
Sending location checks: [10010107]
""","""
Sending location checks: [10011007]
Sending location checks: [10011008]
Sending location checks: [10011007]
Sending location checks: [10011008]
Sending location checks: [10011006]
Sending location checks: [10011901]
Sending location checks: [10011902]
Sending location checks: [10011903]
Sending location checks: [10011904]
Sending location checks: [10012113]
Sending location checks: [10012107]
Sending location checks: [10010102]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10011005]
Sending location checks: [10011001]
Sending location checks: [10011901]
Sending location checks: [10011003]
Sending location checks: [10011901]
Sending location checks: [10011902]
Sending location checks: [10011903]
Sending location checks: [10012108]
Sending location checks: [10012108]
Sending location checks: [10012104]
Sending location checks: [10012114]
Sending location checks: [10012107]
Sending location checks: [10012112]
Sending location checks: [10012111]
Sending location checks: [10012112]
Sending location checks: [10012107]
Sending location checks: [10012112]
Sending location checks: [10012107]
Sending location checks: [10012113]
New Game
Gonna deactivate all buttons
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 230, items: [NetworkItem { item: 10000022, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #22 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 22\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 231, items: [NetworkItem { item: 10000023, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #23 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 23\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 232, items: [NetworkItem { item: 10000024, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #24 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 24\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 233, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
Sending location checks: [10010303]
Sending location checks: [10012304]
Sending location checks: [10012404]
Sending location checks: [10012408]
Sending location checks: [10012407]
Sending location checks: [10012408]
Sending location checks: [10012404]
Sending location checks: [10012403]
Sending location checks: [10012402]
Sending location checks: [10012409]
Sending location checks: [10012405]
Sending location checks: [10012405]
Sending location checks: [10012402]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 234, items: [NetworkItem { item: 10000025, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #25 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 25\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 235, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
Sending location checks: [10010303]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 236, items: [NetworkItem { item: 10000023, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #23 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 23\" to Player1" }] }
Sending location checks: [10012304]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 237, items: [NetworkItem { item: 10000024, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #24 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 24\" to Player1" }] }
Sending location checks: [10012404]
Sending location checks: [10012403]
Sending location checks: [10012506]
Sending location checks: [10012403]
Sending location checks: [10012402]
Sending location checks: [10012409]
Sending location checks: [10012503]
Sending location checks: [10012502]
Sending location checks: [10012503]
Sending location checks: [10012502]
Sending location checks: [10012502]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 238, items: [NetworkItem { item: 10000024, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #24 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 24\" to Player1" }] }
Sending location checks: [10010102]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 239, items: [NetworkItem { item: 10000025, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #25 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 25\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 240, items: [NetworkItem { item: 10000026, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #26 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 26\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 241, items: [NetworkItem { item: 10000027, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #27 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 27\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 242, items: [NetworkItem { item: 10000002, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #2 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 2\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 243, items: [NetworkItem { item: 10000015, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #15 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 15\" to Player1" }] }
Sending location checks: [10010202]
Sending location checks: [10010207]
Sending location checks: [10011501]
Sending location checks: [10011504]
Sending location checks: [10012705]
Sending location checks: [10012706]
Sending location checks: [10012705]
Sending location checks: [10012702]
New Game
Gonna deactivate all buttons
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 244, items: [NetworkItem { item: 10000028, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #28 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 28\" to Player1" }] }
Sending location checks: [10010105]
Sending location checks: [10010104]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 245, items: [NetworkItem { item: 10000029, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #29 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 29\" to Player1" }] }
Sending location checks: [10010105]
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 246, items: [NetworkItem { item: 10000030, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #30 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 30\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 247, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
Sending location checks: [10010303]
Sending location checks: [10010308]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 248, items: [NetworkItem { item: 10000023, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #23 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 23\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 249, items: [NetworkItem { item: 10000022, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #22 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 22\" to Player1" }] }
Sending location checks: [10010308]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 250, items: [NetworkItem { item: 10000012, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #12 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 12\" to Player1" }] }
Sending location checks: [10012304]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 251, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 252, items: [NetworkItem { item: 10000012, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #12 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 12\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010303]
Sending location checks: [10010308]
Sending location checks: [10010303]
Sending location checks: [10010308]
Sending location checks: [10010306]
Sending location checks: [10010305]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 253, items: [NetworkItem { item: 10000011, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #11 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 11\" to Player1" }] }
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 254, items: [NetworkItem { item: 10000028, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #28 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 28\" to Player1" }] }
Sending location checks: [10010102]
"""]

log_data_inf_wall_jump = ["""
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 207, items: [NetworkItem { item: 9999991, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #-9 in-game
Archipelago: setting wall jump to 3
Archipelago: setting ledge grab to -1
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Progressive Wall Jump\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 208, items: [NetworkItem { item: 9999991, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #-9 in-game
Archipelago: setting wall jump to 4
Archipelago: setting ledge grab to -1
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Progressive Wall Jump\" to Player1" }] }
Sending location checks: [10010104]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 209, items: [NetworkItem { item: 10000002, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #2 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 2\" to Player1" }] }
Sending location checks: [10010207]
Sending location checks: [10010205]
Sending location checks: [10010207]
Sending location checks: [10010206]
Sending location checks: [10010207]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 210, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010303]
Sending location checks: [10010309]
Sending location checks: [10010304]
Sending location checks: [10010303]
Sending location checks: [10010303]
Sending location checks: [10010308]
Sending location checks: [10010306]
Sending location checks: [10010306]
Sending location checks: [10010308]
Sending location checks: [10010301]
Sending location checks: [10010305]
Sending location checks: [10010306]
Sending location checks: [10010308]
Sending location checks: [10010301]
Sending location checks: [10010306]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 211, items: [NetworkItem { item: 10000004, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #4 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 4\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010104]
Sending location checks: [10010104]
Sending location checks: [10010404]
Sending location checks: [10010404]
Sending location checks: [10010404]
Sending location checks: [10010404]
Sending location checks: [10010405]
Sending location checks: [10010401]
Sending location checks: [10010403]
Sending location checks: [10010401]
Sending location checks: [10010401]
Sending location checks: [10010405]
Sending location checks: [10010409]
Sending location checks: [10010405]
Sending location checks: [10010401]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 212, items: [NetworkItem { item: 10000005, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #5 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 5\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 213, items: [NetworkItem { item: 10000004, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #4 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 4\" to Player1" }] }
Sending location checks: [10010404]
Sending location checks: [10010405]
Sending location checks: [10010403]
Sending location checks: [10010502]
Sending location checks: [10010504]
Sending location checks: [10010503]
Sending location checks: [10010505]
Sending location checks: [10010506]
Sending location checks: [10010502]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 214, items: [NetworkItem { item: 10000006, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #6 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 6\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010605]
Sending location checks: [10010104]
Sending location checks: [10010605]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 215, items: [NetworkItem { item: 60000000, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #50000000 in-game
Archipelago: setting wall jump to 0
Archipelago: setting ledge grab to 0
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Disable Wall Ledge\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 216, items: [NetworkItem { item: 60000005, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #50000005 in-game
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Disable Swim\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 217, items: [NetworkItem { item: 60000010, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #50000010 in-game
Archipelago: setting jump pads to 0
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Disable Jumppads\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 218, items: [NetworkItem { item: 9999991, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #-9 in-game
Archipelago: setting wall jump to 5
Archipelago: setting ledge grab to -1
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Progressive Wall Jump\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 219, items: [NetworkItem { item: 9999991, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #-9 in-game
Archipelago: setting wall jump to 6
Archipelago: setting ledge grab to -1
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Progressive Wall Jump\" to Player1" }] }
New Game
Gonna deactivate all buttons
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 220, items: [NetworkItem { item: 10000007, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #7 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 7\" to Player1" }] }
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 221, items: [NetworkItem { item: 10000008, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #8 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 8\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 222, items: [NetworkItem { item: 10000009, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #9 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 9\" to Player1" }] }
Sending location checks: [10010106]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 223, items: [NetworkItem { item: 10000010, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #10 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 10\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10011005]
Sending location checks: [10010107]
Sending location checks: [10010101]
Sending location checks: [10000101]
Sending location checks: [10010101]
Sending location checks: [10010107]
Sending location checks: [10010106]
Sending location checks: [10011009]
Sending location checks: [10011009]
Sending location checks: [10011001]
Sending location checks: [10011009]
Sending location checks: [10011009]
Sending location checks: [10011001]
Sending location checks: [10001001]
Sending location checks: [10011001]
Sending location checks: [10011001]
Sending location checks: [10001001]
Sending location checks: [10011001]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 224, items: [NetworkItem { item: 10000011, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #11 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 11\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 225, items: [NetworkItem { item: 10000012, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #12 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 12\" to Player1" }] }
Sending location checks: [10011104]
Sending location checks: [10011106]
Sending location checks: [10011103]
Sending location checks: [10011105]
Sending location checks: [10011201]
Sending location checks: [10011202]
Sending location checks: [10010102]
Sending location checks: [10011104]
Sending location checks: [10011106]
Sending location checks: [10011103]
Sending location checks: [10011105]
Sending location checks: [10011201]
Sending location checks: [10011204]
Sending location checks: [10011201]
Sending location checks: [10001201]
Sending location checks: [10011201]
Sending location checks: [10011202]
Sending location checks: [10011203]
Sending location checks: [10011202]
Sending location checks: [10011204]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 226, items: [NetworkItem { item: 10000013, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #13 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 13\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 227, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
Sending location checks: [10010303]
Sending location checks: [10011301]
Sending location checks: [10010303]
Sending location checks: [10011303]
Sending location checks: [10010303]
Sending location checks: [10011304]
Sending location checks: [10011302]
Sending location checks: [10011304]
Sending location checks: [10010308]
Sending location checks: [10010102]
Sending location checks: [10010303]
Sending location checks: [10010308]
Sending location checks: [10010301]
Sending location checks: [10010301]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 228, items: [NetworkItem { item: 10000014, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #14 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 14\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 229, items: [NetworkItem { item: 10000015, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #15 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 15\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 230, items: [NetworkItem { item: 10000002, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #2 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 2\" to Player1" }] }
Sending location checks: [10010202]
Sending location checks: [10010207]
Sending location checks: [10011501]
Sending location checks: [10011502]
Sending location checks: [10001501]
Sending location checks: [10011502]
Sending location checks: [10011503]
Sending location checks: [10001501]
Sending location checks: [10011502]
Sending location checks: [10001501]
Sending location checks: [10011502]
Sending location checks: [10011503]
Sending location checks: [10011503]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 231, items: [NetworkItem { item: 10000016, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #16 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 16\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010102]
Sending location checks: [10010105]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 232, items: [NetworkItem { item: 10000002, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #2 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 2\" to Player1" }] }
Sending location checks: [10010104]
Sending location checks: [10010207]
Sending location checks: [10010205]
Sending location checks: [10011603]
Sending location checks: [10011602]
Sending location checks: [10011601]
Sending location checks: [10011602]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 233, items: [NetworkItem { item: 10000017, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #17 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 17\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 234, items: [NetworkItem { item: 10000016, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #16 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 16\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 235, items: [NetworkItem { item: 10000002, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #2 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 2\" to Player1" }] }
Sending location checks: [10010207]
Sending location checks: [10011703]
Sending location checks: [10011703]
Sending location checks: [10011701]
Sending location checks: [10011704]
Sending location checks: [10011701]
Sending location checks: [10011601]
Sending location checks: [10011701]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 236, items: [NetworkItem { item: 10000018, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #18 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 18\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 237, items: [NetworkItem { item: 10000004, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #4 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 4\" to Player1" }] }
Sending location checks: [10010404]
Sending location checks: [10010405]
Sending location checks: [10010409]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 238, items: [NetworkItem { item: 10000019, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #19 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 19\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 239, items: [NetworkItem { item: 10000009, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #9 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 9\" to Player1" }] }
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010103]
Sending location checks: [10010106]
Sending location checks: [10010106]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 240, items: [NetworkItem { item: 10000008, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #8 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 8\" to Player1" }] }
Sending location checks: [10010807]
Sending location checks: [10010806]
Sending location checks: [10010905]
Sending location checks: [10010903]
Sending location checks: [10010901]
Sending location checks: [10010902]
Sending location checks: [10010907]
Sending location checks: [10011902]
Sending location checks: [10011903]
Sending location checks: [10011904]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 241, items: [NetworkItem { item: 10000020, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #20 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 20\" to Player1" }] }
Sending location checks: [10010102]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 242, items: [NetworkItem { item: 10000021, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #21 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 21\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 243, items: [NetworkItem { item: 10000010, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #10 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 10\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 244, items: [NetworkItem { item: 10000011, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #11 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 11\" to Player1" }] }
Sending location checks: [10011005]
Sending location checks: [10011104]
Sending location checks: [10011106]
Sending location checks: [10011107]
Sending location checks: [10011003]
Sending location checks: [10001002]
Sending location checks: [10011003]
Sending location checks: [10001002]
Sending location checks: [10011003]
Sending location checks: [10001002]
Sending location checks: [10011003]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 245, items: [NetworkItem { item: 10000020, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #20 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 20\" to Player1" }] }
Sending location checks: [10012009]
Sending location checks: [10012108]
Sending location checks: [10012107]
Sending location checks: [10012113]
Sending location checks: [10012107]
Sending location checks: [10012106]
Sending location checks: [10012107]
Sending location checks: [10012101]
Sending location checks: [10012102]
Sending location checks: [10012110]
Sending location checks: [10012112]
Sending location checks: [10012111]
Sending location checks: [10012112]
Sending location checks: [10012004]
Sending location checks: [10012003]
Sending location checks: [10012115]
Sending location checks: [10012007]
Sending location checks: [10012003]
Sending location checks: [10012001]
Sending location checks: [10012002]
Sending location checks: [10012003]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 246, items: [NetworkItem { item: 10000022, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #22 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 22\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 247, items: [NetworkItem { item: 10000023, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #23 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 23\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 248, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
Sending location checks: [10010303]
Sending location checks: [10010308]
Sending location checks: [10012304]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 249, items: [NetworkItem { item: 10000024, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #24 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 24\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 250, items: [NetworkItem { item: 10000025, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #25 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 25\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 251, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
Sending location checks: [10010303]
Sending location checks: [10010308]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 252, items: [NetworkItem { item: 10000023, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #23 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 23\" to Player1" }] }
Sending location checks: [10012304]
Sending location checks: [10012404]
Sending location checks: [10012403]
Sending location checks: [10012402]
Sending location checks: [10012409]
Sending location checks: [10012503]
Sending location checks: [10012502]
Sending location checks: [10012504]
Sending location checks: [10012504]
Sending location checks: [10012501]
Sending location checks: [10012504]
Sending location checks: [10012501]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 253, items: [NetworkItem { item: 10000026, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #26 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 26\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 254, items: [NetworkItem { item: 10000027, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #27 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 27\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 255, items: [NetworkItem { item: 10000028, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #28 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 28\" to Player1" }] }
Sending location checks: [10010105]
Sending location checks: [10010105]
Sending location checks: [10010104]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 256, items: [NetworkItem { item: 10000004, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #4 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 4\" to Player1" }] }
Sending location checks: [10010408]
Sending location checks: [10012801]
Sending location checks: [10012802]
Sending location checks: [10012812]
Sending location checks: [10012802]
Sending location checks: [10012812]
Sending location checks: [10012801]
Sending location checks: [10010408]
Sending location checks: [10012801]
Sending location checks: [10012817]
Sending location checks: [10012805]
Sending location checks: [10012806]
Sending location checks: [10010102]
Sending location checks: [10010105]
Sending location checks: [10010104]
Sending location checks: [10010408]
Sending location checks: [10012801]
Sending location checks: [10012802]
Sending location checks: [10012815]
Sending location checks: [10012819]
Sending location checks: [10012815]
Sending location checks: [10012816]
Sending location checks: [10012815]
Sending location checks: [10012814]
Sending location checks: [10012809]
Sending location checks: [10012814]
Sending location checks: [10012811]
Sending location checks: [10012813]
Sending location checks: [10010102]
New Game
Gonna deactivate all buttons
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 257, items: [NetworkItem { item: 10000030, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #30 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 30\" to Player1" }] }
Sending location checks: [10010102]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 258, items: [NetworkItem { item: 10000003, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #3 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 3\" to Player1" }] }
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 259, items: [NetworkItem { item: 10000011, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #11 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 11\" to Player1" }] }
Sending location checks: [10010303]
Sending location checks: [10011105]
Sending location checks: [10011101]
ReceivedItems message
Archipelago ServerMessage::ReceivedItems: ReceivedItems { index: 260, items: [NetworkItem { item: 10000012, location: -1, player: 0, flags: 0 }] }
APAPAP Trigger Cluster #12 in-game
Gonna activate all buttons
Gonna deactivate all buttons
PrintJSON message
Archipelago ServerMessage::PrintJSON: Text { data: [Text { text: "Cheat console: sending \"Trigger Cluster 12\" to Player1" }] }
Sending location checks: [10011108]
Sending location checks: [10011205]
Sending location checks: [10011101]
Sending location checks: [10011101]
Sending location checks: [10011108]
Sending location checks: [10010308]
Sending location checks: [10010308]
Sending location checks: [10011108]
Sending location checks: [10001101]
Sending location checks: [10011205]
Sending location checks: [10013006]
Sending location checks: [10013013]
Sending location checks: [10013009]
Sending location checks: [10013008]
Sending location checks: [10013004]
Sending location checks: [10013011]
Sending location checks: [10013004]
Sending location checks: [10013008]
Sending location checks: [10013007]
Sending location checks: [10011204]
Sending location checks: [10011202]
Sending location checks: [10011203]
Sending location checks: [10010302]
Sending location checks: [10011202]
Sending location checks: [10013007]
Sending location checks: [10013005]
Sending location checks: [10013004]
Sending location checks: [10013010]
Sending location checks: [10013001]
Sending location checks: [10013010]
Sending location checks: [10013003]
Sending location checks: [10013001]
Sending location checks: [10013002]
Sending location checks: [10013006]
Sending location checks: [10013013]
Sending location checks: [10013007]
Sending location checks: [10013008]
""",
"""
Sending location checks: [10012404]
Sending location checks: [10012303]
"""]




def find_connections(clusters, data):
    # Find connections between clusters
    cluster_keys = sorted(clusters.keys())
    connections = set()
    for i in range(len(cluster_keys)):
        for j in range(len(cluster_keys)):
            if i == j:
                continue
            c1 = cluster_keys[i]
            c2 = cluster_keys[j]
            # Check if there's any edge from nodes1 to nodes2
            found_connection = False
            for n1 in clusters[c1]:
                for n2 in clusters[c2]:
                    if (n1,n2) in data:
                        connections.add((c1, c2))
                        found_connection = True
                        break
                if found_connection:
                    break
    return connections

# Find connections between clusters
connections_vanilla = find_connections(clusters, data)

connections_jumppad = find_connections(clusters, create_connections_from_logs(log_data_jumppads))
connections_ledge_grab = find_connections(clusters, create_connections_from_logs(log_data_ledge_grab))
connections_swim = find_connections(clusters, create_all_pairs_from_logs(log_data_swim))
conneections_one_wall_jump = find_connections(clusters, create_connections_from_logs(log_data_one_wall_jump))
conneections_inf_wall_jump = find_connections(clusters, create_connections_from_logs(log_data_inf_wall_jump))

connections_jumppad = set([ (a,b) for (a,b) in connections_jumppad if (a,b) not in connections_vanilla])
connections_ledge_grab = set([ (a,b) for (a,b) in connections_ledge_grab if (a,b) not in connections_vanilla])
connections_swim = set([ (a,b) for (a,b) in connections_swim if (a,b) not in connections_vanilla])
connections_one_wall_jump = set([ (a,b) for (a,b) in conneections_one_wall_jump if (a,b) not in connections_vanilla])

connections_inf_wall_jump = set([ (a,b) for (a,b) in conneections_inf_wall_jump if (a,b) not in connections_vanilla and (a,b) not in connections_one_wall_jump])

def dump_json(obj, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)

# prepare clusters: keys as strings for valid JSON object keys, node lists sorted
clusters_json = {int(k): sorted(v) for k, v in clusters.items()}
dump_json(clusters_json, "data/clusters.json")

# helper to convert connection sets of tuples to sorted lists
def connections_to_list(conns):
    return [[a, b] for a, b in sorted(conns)]

dump_json(connections_to_list(connections_vanilla), "data/connections_vanilla.json")
dump_json(connections_to_list(connections_jumppad), "data/connections_jumppad.json")
dump_json(connections_to_list(connections_ledge_grab), "data/connections_ledge_grab.json")
dump_json(connections_to_list(connections_swim), "data/connections_swim.json")
dump_json(connections_to_list(connections_one_wall_jump), "data/connections_one_wall_jump.json")
dump_json(connections_to_list(connections_inf_wall_jump), "data/connections_inf_wall_jump.json")

# find clusters not reachable from node 10010102 using all connection types
start_node = 10010102
start_cluster = next((k for k, nodes in clusters.items() if start_node in nodes), None)
if start_cluster is None:
    print("Start node", start_node, "is not in any cluster")
else:
    all_connections = set().union(
        connections_vanilla,
        connections_jumppad,
        connections_ledge_grab,
        connections_swim,
        connections_one_wall_jump,
        connections_inf_wall_jump,
    )

    # build cluster-level adjacency
    cadj = {k: set() for k in clusters.keys()}
    for a, b in all_connections:
        cadj.setdefault(a, set()).add(b)

    # BFS/DFS from start_cluster
    visited = set()
    stack = [start_cluster]
    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        for w in cadj.get(v, ()):
            if w not in visited:
                stack.append(w)

    unreachable_clusters = set(clusters.keys()) - visited

    # compute reachable node ids (locations) and unreachable locations from all_locations
    reachable_nodes = set()
    for k in visited:
        reachable_nodes.update(clusters.get(k, []))

    unreachable_locations = sorted([loc for loc in all_locations if loc not in reachable_nodes])

    print("start_cluster:", start_cluster)
    print("reachable clusters count:", len(visited))
    print("unreachable clusters count:", len(unreachable_clusters))
    print("unreachable cluster keys (with nodes):")
    for k in sorted(unreachable_clusters):
        print(k, clusters[k])

    print()
    print("reachable node count:", len(reachable_nodes))
    print("unreachable locations from all_locations count:", len(unreachable_locations))
    print("unreachable locations from all_locations:")
    # for loc in unreachable_locations:
    #     print(loc)