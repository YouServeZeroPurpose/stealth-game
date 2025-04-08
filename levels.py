#     EDITOR NUMBER CODE: 
#
# 0: Nothing
# 1: Wall block
# 2: Enemy spawn(goes up at first, and walks in a 7 long block square, his position is in the middle of a 2*2 square where the number "2" in the editor is in the top left corner)
# 3: Horizontal laser(takes up 2 blocks of space, the number "3" in the editor is the left part)
# 4: Vertical laser(takes up 2 blocks of space, the nmumber "4" in the editor is in the top part)
# 5: Key
# 6: Vault door(takes up 2 blocks of space horizontally, the number "6" in the editor is in the left part)
# 7: Money bag(its position is in the middle of a 2*2 square where the number "7" in the editor is in the top left corner)
# 8: Player(his position is in the middle of a 2*2 square where the number "8" in the editor is in the top left corner)


levels = {
'lvl1': [1111111111111111,
        1800000000100001,
        1000000000100001,
        1001111100107001,
        1001000100100001,
        1000000000100001,
        1001000100100001,
        1001111100116011,
        1000000000000001,
        1000000000000001,
        1110011100111001,
        1000011100111001,
        1050011100111001,
        1000011120000001,
        1000011100000001,
        1111111111111111],

'lvl2': [1111111111111111,
        1800000100000001,
        1000000100000001,
        1000000100111001,
        1000000100111001,
        1000000100111001,
        1001111120000001,
        1001000100050001,
        1001700100000001,
        1001000100000001,
        1001000100111001,
        1001000100111001,
        1001160100111001,
        1000000020000001,
        1000000000000001,
        1111111111111111],

'lvl3': [1111111111111111,
        1801070000000001,
        1001000000000001,
        1001000000000001,
        1001111111111601,
        1000000000051001,
        1000000000001001,
        1001100111001301,
        1301100111001001,
        1001100111001001,
        1001120000001301,
        1001100000001001,
        1001111111111001,
        1000000400000001,
        1000000000000001,
        1111111111111111],

'lvl4': [1111111111111111,
        1801000004004001,
        1001070000000001,
        1301000001111601,
        1001111111111001,
        1301050400001301,
        1001000000001001,
        1301111111301301,
        1000040004000001,
        1000000000000001,
        1001110011100111,
        1301113011130111,
        1001110011100111,
        1200402004000111,
        1000000000000111,
        1111111111111111]
}