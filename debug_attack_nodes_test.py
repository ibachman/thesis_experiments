import debug_attack_nodes as dan
import datetime
from interdependent_network_library import *

legacy = True
exp = "2.5"
n_inter = "3"
x_coordinate = 20
y_coordinate = 500
version = 3
model = "RNG"
process_name = "debug"

# load a network
network_system = InterdependentGraph()
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, "networks")

logic_dir = os.path.join(path, "logical_networks")
physical_dir = os.path.join(path, "physical_networks", "links")
interlink_dir = os.path.join(path, "interdependencies", "full_random")
providers_dir = os.path.join(path, "providers")
node_loc_dir = os.path.join(path, "physical_networks", "node_locations")

if legacy:
    logic_title = "legacy_{}".format(csv_title_generator("logic", "20", "500", exp, version=1))
    interlink_title = "legacy_{}".format(csv_title_generator("dependence", "20", "500", exp, n_inter, 6,
                                                             version=1))
    providers_title = "legacy_{}".format(csv_title_generator("providers", "20", "500", exp, n_inter, 6,
                                                             version=1))
else:
    logic_title = csv_title_generator("logic", "20", "500", exp, version=1)
    interlink_title = csv_title_generator("dependence", "20", "500", exp, n_inter, 6, version=1)
    providers_title = csv_title_generator("providers", "20", "500", exp, n_inter, 6, version=1)

nodes_loc_title = csv_title_generator("nodes", x_coordinate, y_coordinate, exp, version=version)
physic_title = csv_title_generator("physic", x_coordinate, y_coordinate, exp, version=version, model=model)
logic_dir = os.path.join(logic_dir, logic_title)
physical_dir = os.path.join(physical_dir, physic_title)
interlink_dir = os.path.join(interlink_dir, interlink_title)
providers_dir = os.path.join(providers_dir, providers_title)
nodes_loc_dir = os.path.join(node_loc_dir, nodes_loc_title)

network_system.create_from_csv(logic_dir, physical_dir, interlink_dir, nodes_loc_dir, providers_csv=providers_dir)
print("{} -- System created {} from:".format(process_name, datetime.datetime.now()))
print("{} -- -> Logical network: {}".format(process_name, logic_dir))
print("{} -- -> Inter-links: {}".format(process_name, interlink_dir))
print("{} -- -> Providers: {}".format(process_name, providers_dir))
print("{} -- -> Physical network: {}".format(process_name, physical_dir))
print("{} -- -> Node allocation: {}".format(process_name, nodes_loc_dir))
# generate random nodes to remove

physical_network = network_system.get_phys()
sample = physical_network.vs['name']
all_nodes_to_delete = dan.get_list_of_nodes_to_attack(sample, 1, len(sample))
#all_nodes_to_delete = dan.get_list_of_nodes_to_attack(sample, 500, len(sample))

tiny_samp = [['p213', 'p1702', 'p331', 'p1606', 'p1940', 'p381', 'p1454', 'p631', 'p77', 'p457', 'p149', 'p73', 'p1977', 'p210', 'p307', 'p305', 'p279', 'p922', 'p1322', 'p1337', 'p686', 'p577', 'p791', 'p1244', 'p78', 'p1395', 'p1138', 'p1594', 'p799', 'p154', 'p1968', 'p424', 'p1280', 'p636', 'p1596', 'p1691', 'p1734', 'p951', 'p750', 'p1652', 'p1600', 'p41', 'p139', 'p1703', 'p1096', 'p1674', 'p712', 'p102', 'p1493', 'p1088', 'p220', 'p1682', 'p1907', 'p985', 'p488', 'p1764', 'p660', 'p1183', 'p604', 'p560', 'p1495', 'p26', 'p1100', 'p18', 'p456', 'p1548', 'p1608', 'p1538', 'p1805', 'p721', 'p1670', 'p283', 'p30', 'p1802', 'p710', 'p1863', 'p781', 'p90', 'p1485', 'p1750', 'p1746', 'p1079', 'p395', 'p269', 'p770', 'p1998', 'p1095', 'p138', 'p950', 'p473', 'p339', 'p711', 'p1629', 'p808', 'p1660', 'p573', 'p590', 'p411', 'p1890', 'p1304', 'p156', 'p779', 'p970', 'p302', 'p221', 'p1930', 'p1858', 'p1663', 'p8', 'p726', 'p1865', 'p1571', 'p106', 'p118', 'p1170', 'p169', 'p1950', 'p1350', 'p290', 'p198', 'p885', 'p321', 'p551', 'p611', 'p1011', 'p1489', 'p1137', 'p1948', 'p903', 'p888', 'p1636', 'p1877', 'p1897', 'p1315', 'p1967', 'p805', 'p1240', 'p1736', 'p261', 'p962', 'p984', 'p344', 'p537', 'p1595', 'p1834', 'p1925', 'p629', 'p1961', 'p1020', 'p494', 'p1412', 'p368', 'p430', 'p1648', 'p656', 'p86', 'p380', 'p1645', 'p550', 'p1427', 'p1749', 'p1726', 'p708', 'p1152', 'p1725', 'p691', 'p795', 'p1531', 'p754', 'p1247', 'p1644', 'p1539', 'p403', 'p92', 'p1659', 'p1980', 'p1780', 'p1332', 'p1411', 'p1205', 'p1862', 'p1699', 'p767', 'p949', 'p558', 'p2', 'p1469', 'p242', 'p887', 'p1431', 'p1242', 'p348', 'p1430', 'p1747', 'p1132', 'p178', 'p1970', 'p182', 'p1872', 'p1216', 'p1217', 'p179', 'p1196', 'p806', 'p607', 'p1717', 'p137', 'p1460', 'p614', 'p732', 'p1766', 'p674', 'p669', 'p1200', 'p661', 'p1388', 'p813', 'p1513', 'p431', 'p654', 'p1848', 'p1413', 'p42', 'p135', 'p1559', 'p1641', 'p17', 'p1387', 'p303', 'p1508', 'p1348', 'p1335', 'p1626', 'p609', 'p1008', 'p155', 'p207', 'p524', 'p1777', 'p610', 'p1166', 'p472', 'p773', 'p1434', 'p204', 'p1133', 'p1979', 'p363', 'p1157', 'p588', 'p452', 'p1786', 'p385', 'p332', 'p1768', 'p1300', 'p124', 'p1187', 'p1077', 'p872', 'p1072', 'p1616', 'p1779', 'p1468', 'p405', 'p1576', 'p1630', 'p552', 'p1651', 'p1165', 'p1053', 'p1969', 'p954', 'p720', 'p634', 'p485', 'p16', 'p1221', 'p1494', 'p1895', 'p1176', 'p324', 'p1194', 'p824', 'p426', 'p608', 'p1325', 'p1243', 'p406', 'p58', 'p1686', 'p1381', 'p1795', 'p673', 'p404', 'p928', 'p995', 'p1578', 'p690', 'p1108', 'p229', 'p835', 'p506', 'p812', 'p32', 'p509', 'p247', 'p172', 'p1718', 'p1655', 'p67', 'p1666', 'p144', 'p167', 'p1499', 'p448', 'p1668', 'p864', 'p250', 'p1179', 'p1482', 'p988', 'p1045', 'p1338', 'p1479', 'p532', 'p1638', 'p1971', 'p113', 'p829', 'p1035', 'p843', 'p1130', 'p1410', 'p1602', 'p409', 'p61', 'p382', 'p265', 'p1885', 'p733', 'p371', 'p1401', 'p538', 'p612', 'p20', 'p1934', 'p352', 'p1364', 'p1463', 'p727', 'p549', 'p796', 'p556', 'p1523', 'p378', 'p1146', 'p1175', 'p450', 'p40', 'p1211', 'p763', 'p1590', 'p1446', 'p311', 'p626', 'p53', 'p1667', 'p161', 'p1611', 'p486', 'p880', 'p1844', 'p235', 'p275', 'p74', 'p1882', 'p1084', 'p441', 'p103', 'p59', 'p873', 'p1436', 'p1675', 'p1773', 'p1447', 'p787', 'p232', 'p1856', 'p1312', 'p1453', 'p1199', 'p1815', 'p239', 'p890', 'p913', 'p1302', 'p833', 'p1422', 'p1534', 'p1310', 'p960', 'p1145', 'p975', 'p1226', 'p904', 'p639', 'p858', 'p1334', 'p1625', 'p1060', 'p454', 'p1724', 'p445', 'p675', 'p1867', 'p1679', 'p170', 'p670', 'p671', 'p1957', 'p211', 'p798', 'p999', 'p972', 'p1836', 'p1249', 'p1556', 'p1419', 'p1093', 'p112', 'p1721', 'p725', 'p1708', 'p1125', 'p68', 'p1363', 'p1171', 'p97', 'p190', 'p25', 'p516', 'p81', 'p1222', 'p1728', 'p1841', 'p1333', 'p814', 'p248', 'p955', 'p886', 'p1700', 'p1220', 'p340', 'p1978', 'p1025', 'p65', 'p1583', 'p1287', 'p1701', 'p920', 'p1937', 'p55', 'p1994', 'p38', 'p1580', 'p905', 'p1286', 'p809', 'p1013', 'p1662', 'p603', 'p1355', 'p1393', 'p865', 'p837', 'p1225', 'p1229', 'p1917', 'p613', 'p469', 'p1261', 'p884', 'p1215', 'p164', 'p1568', 'p1255', 'p1490', 'p521', 'p1291', 'p684', 'p370', 'p827', 'p1068', 'p470', 'p1846', 'p1120', 'p1832', 'p1005', 'p129', 'p788', 'p1254', 'p937', 'p1048', 'p505', 'p1552', 'p1910', 'p1359', 'p35', 'p1837', 'p1299', 'p941', 'p366', 'p330', 'p1981', 'p399', 'p547', 'p1619', 'p142', 'p1047', 'p627', 'p599', 'p1308', 'p244', 'p786', 'p719', 'p34', 'p253', 'p1689', 'p1516', 'p372', 'p1174', 'p1377', 'p500', 'p692', 'p862', 'p72', 'p150', 'p1792', 'p24', 'p1181', 'p1591', 'p911', 'p1962', 'p127', 'p1356', 'p62', 'p1055', 'p1615', 'p336', 'p151', 'p934', 'p1813', 'p195', 'p518', 'p508', 'p383', 'p1266', 'p1720', 'p1695', 'p205', 'p37', 'p600', 'p713', 'p878', 'p1713', 'p1722', 'p700', 'p1751', 'p392', 'p832', 'p1642', 'p1444', 'p841', 'p936', 'p238', 'p254', 'p1272', 'p1714', 'p437', 'p165', 'p1521', 'p1745', 'p852', 'p23', 'p879', 'p166', 'p1016', 'p953', 'p1892', 'p1081', 'p1052', 'p756', 'p1126', 'p745', 'p907', 'p504', 'p591', 'p743', 'p1506', 'p272', 'p1438', 'p1214', 'p1800', 'p351', 'p1891', 'p14', 'p1030', 'p1665', 'p716', 'p1357', 'p1681', 'p1517', 'p742', 'p1092', 'p337', 'p1303', 'p764', 'p1184', 'p1314', 'p1127', 'p1601', 'p1250', 'p1472', 'p45', 'p628', 'p400', 'p707', 'p1737', 'p1269', 'p1178', 'p1711', 'p1753', 'p665', 'p180', 'p1007', 'p1063', 'p927', 'p1847', 'p1119', 'p48', 'p288', 'p435', 'p296', 'p1966', 'p775', 'p929', 'p989', 'p1098', 'p1985', 'p1253', 'p1323', 'p1640', 'p1586', 'p1160', 'p617', 'p1104', 'p1886', 'p1193', 'p79', 'p618', 'p689', 'p702', 'p1484', 'p714', 'p1871', 'p1859', 'p652', 'p926', 'p688', 'p1425', 'p1471', 'p1894', 'p1514', 'p650', 'p1944', 'p28', 'p306', 'p1901', 'p1827', 'p482', 'p355', 'p187', 'p1903', 'p893', 'p875', 'p564', 'p327', 'p1588', 'p369', 'p1673', 'p56', 'p1087', 'p1149', 'p1828', 'p1812', 'p562', 'p944', 'p1352', 'p1565', 'p554', 'p718', 'p513', 'p851', 'p1938', 'p1167', 'p1624', 'p443', 'p844', 'p641', 'p287', 'p1283', 'p777', 'p1928', 'p1420', 'p1346', 'p1790', 'p638', 'p122', 'p414', 'p1912', 'p1039', 'p623', 'p1927', 'p1796', 'p1876', 'p938', 'p863', 'p1018', 'p1379', 'p1504', 'p811', 'p658', 'p1705', 'p527', 'p1256', 'p1339', 'p1974', 'p1313', 'p361', 'p1964', 'p680', 'p1078', 'p359', 'p222', 'p1676', 'p4', 'p1069', 'p364', 'p981', 'p1557', 'p762', 'p1905', 'p1224', 'p1452', 'p1475', 'p1972', 'p1941', 'p1739', 'p1210', 'p807', 'p460', 'p855', 'p1415', 'p1661', 'p1403', 'p602', 'p96', 'p1515', 'p297', 'p1817', 'p894', 'p1954', 'p548', 'p1532', 'p1549', 'p1143', 'p1354', 'p176', 'p1083', 'p251', 'p201', 'p615', 'p1437', 'p1605', 'p1637', 'p736', 'p1887', 'p234', 'p1139', 'p657', 'p192', 'p664', 'p1455', 'p1597', 'p1271', 'p856', 'p117', 'p861', 'p867', 'p1124', 'p991', 'p301', 'p853', 'p75', 'p1617', 'p1519', 'p1182', 'p891', 'p567', 'p1208', 'p1435', 'p1481', 'p423', 'p461', 'p544', 'p319', 'p1231', 'p9', 'p1631', 'p1628', 'p1330', 'p1845', 'p1443', 'p1118', 'p1155', 'p1329', 'p31', 'p536', 'p249', 'p616', 'p1698', 'p108', 'p1347']
]
# run on
iter_res_2 = dan.new_attack_nodes(network_system, 1, tiny_samp)
iter_res_1 = dan.old_attack_nodes(network_system, 1, tiny_samp)

for i in range(1):
    print("({}) {} ||| {}".format(i, iter_res_1[i], iter_res_2[i]))

# Probar mirando las redes lógicas
