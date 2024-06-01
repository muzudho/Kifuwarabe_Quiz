import datetime


class BoardHelper():
    """盤操作を助ける機能集"""


    @staticmethod
    def get_horizontal_sq_by_file_rank(file, rank):
        """筋番号と段番号とマス番号は 0 から始まるとし、
        筋番号と段番号を渡すと、横型のマス番号を返します
        """
        return 9 * rank + (8 - file)


    @staticmethod
    def get_file_rank_by_horizontal_sq(horizontal_serial_sq):
        """筋番号と段番号とマス番号は 0 から始まるとし、
        横型のマス番号を渡すと、筋番号と段番号を返します
        """
        file = (8 - horizontal_serial_sq % 9)
        rank = horizontal_serial_sq // 9

        return (file, rank)


    @staticmethod
    def jsa_to_sq(jsa_sq):
        """プロ棋士も使っているマス番号の書き方は
        コンピューターには使いづらいので、
        0 から始まるマスの通し番号に変換します

        豆知識：　十の位を筋、一の位を段とするマス番号は、
                将棋の棋士も棋譜に用いている記法です。
                JSA は日本将棋連盟（Japan Shogi Association）

        Parameters
        ----------
        jsa_sq : int
            筋と段は 1 から始まる整数とし、
            十の位を筋、一の位を段とするマス番号
        """

        file = jsa_sq // 10 - 1
        rank = jsa_sq % 10 - 1

        return BoardHelper.get_horizontal_sq_by_file_rank(file, rank)


    @staticmethod
    def sq_to_jsa(horizontal_serial_sq):
        """0 から始まるマスの通し番号は読みずらいので、
        十の位を筋、一の位を段になるよう変換します。
        これは将棋の棋士も棋譜に用いている記法です。
        JSA は日本将棋連盟（Japan Shogi Association）

        Parameters
        ----------
        serial_sq : int
            0 から始まるマスの通し番号
        """

        (file,
         rank) = BoardHelper.get_file_rank_by_horizontal_sq(horizontal_serial_sq)

        return 10 * (file + 1) + (rank + 1)


class DebugHelper():
    """デバッグを助ける機能集"""



    @staticmethod
    def stringify_3characters_horizontal_board(squares):
        """１マスに３桁を表示できる横型の表

        Parameters
        ----------
        squares : [81]
            ８１マスの表
        """

        # 長い変数名を短くする
        s = squares

        return f"""\
  9   8   7   6   5   4   3   2   1
+---+---+---+---+---+---+---+---+---+
|{s[0]:3}|{s[1]:3}|{s[2]:3}|{s[3]:3}|{s[4]:3}|{s[5]:3}|{s[6]:3}|{s[7]:3}|{s[8]:3}| 一
+---+---+---+---+---+---+---+---+---+
|{s[9]:3}|{s[10]:3}|{s[11]:3}|{s[12]:3}|{s[13]:3}|{s[14]:3}|{s[15]:3}|{s[16]:3}|{s[17]:3}| 二
+---+---+---+---+---+---+---+---+---+
|{s[18]:3}|{s[19]:3}|{s[20]:3}|{s[21]:3}|{s[22]:3}|{s[23]:3}|{s[24]:3}|{s[25]:3}|{s[26]:3}| 三
+---+---+---+---+---+---+---+---+---+
|{s[27]:3}|{s[28]:3}|{s[29]:3}|{s[30]:3}|{s[31]:3}|{s[32]:3}|{s[33]:3}|{s[34]:3}|{s[35]:3}| 四
+---+---+---+---+---+---+---+---+---+
|{s[36]:3}|{s[37]:3}|{s[38]:3}|{s[39]:3}|{s[40]:3}|{s[41]:3}|{s[42]:3}|{s[43]:3}|{s[44]:3}| 五
+---+---+---+---+---+---+---+---+---+
|{s[45]:3}|{s[46]:3}|{s[47]:3}|{s[48]:3}|{s[49]:3}|{s[50]:3}|{s[51]:3}|{s[52]:3}|{s[53]:3}| 六
+---+---+---+---+---+---+---+---+---+
|{s[54]:3}|{s[55]:3}|{s[56]:3}|{s[57]:3}|{s[58]:3}|{s[59]:3}|{s[60]:3}|{s[61]:3}|{s[62]:3}| 七
+---+---+---+---+---+---+---+---+---+
|{s[63]:3}|{s[64]:3}|{s[65]:3}|{s[66]:3}|{s[67]:3}|{s[68]:3}|{s[69]:3}|{s[70]:3}|{s[71]:3}| 八
+---+---+---+---+---+---+---+---+---+
|{s[72]:3}|{s[73]:3}|{s[74]:3}|{s[75]:3}|{s[76]:3}|{s[77]:3}|{s[78]:3}|{s[79]:3}|{s[80]:3}| 九
+---+---+---+---+---+---+---+---+---+
"""


class Kifuwarabe():
    """きふわらべのソースコード"""


    @staticmethod
    def main(file_name, n_sq):
        """メイン・プログラム

        Parameters
        ----------
        file_name : str
            出力ファイル名
        n_sq : int
            桂馬（kNight）のいるマス番号（SQuare）
        """

        # 盤の横幅
        board_width = 9

        # 利きのあるマス番号の集合
        effect_sq_set = set()
        #
        #   👆　豆知識：　チェスでは利きは control、コンピューター将棋では利きは effect。
        #
        #               利きを３駒関係の特徴として加えたことで有名な将棋エンジンに　第２４回世界コンピュータ将棋選手権に参加した AWAKE があるが、
        #               当時のやねさんのブログによると、
        #               この頃の AWAKE の巨瀬さんは利きを attack と呼び、
        #               Apery の平岡さんは利きを effect と呼び、
        #               無明やオズのアメリカ人の Wada さんは利きを control と呼び、
        #               Stockfishの作者はイタリア系かノルウェー系だからか利きを effect と呼んでいる。
        #               英語のネイティブでない開発者が多いからか、コンピューター将棋では effect で落ち着いた。
        #
        #               📖 [AWAKEのKPEの実装に向けて その1](https://yaneuraou.yaneu.com/2014/12/25/awake%E3%81%AEkpe%E3%81%AE%E5%AE%9F%E8%A3%85%E3%81%AB%E5%90%91%E3%81%91%E3%81%A6-%E3%81%9D%E3%81%AE1/)
        #

        # 桂馬の右の方の利き（effect）
        #
        #   👇　豆知識：　２段上の右マスは、盤の横幅２つ分より１つ手前
        #
        right_effect_sq = n_sq - (2 * board_width - 1)
        effect_sq_set.add(right_effect_sq)

        # 桂馬の左の方の利き
        #
        #   👇　豆知識：　２段上の左マスは、盤の横幅２つ分より１つ奥
        #
        left_effect_sq = n_sq - (2 * board_width + 1)
        effect_sq_set.add(left_effect_sq)

        # デバッグ出力
        print(f"""[{datetime.datetime.now()}] write `{file_name}` file...
    n_masu:{BoardHelper.sq_to_jsa(n_sq)}  left_effect_masu:{BoardHelper.sq_to_jsa(left_effect_sq)}  right_effect_masu:{BoardHelper.sq_to_jsa(right_effect_sq)}
""")


        with open(file_name, 'w', encoding='utf-8') as f:

            # １マスに３桁の文字列が入るとし、その８１マス分
            squares = ['   '] * 81

            serial_effect_index = 0

            for target_rank in range(0,9):
                for target_file in reversed(range(0,9)):
                    target_sq = BoardHelper.get_horizontal_sq_by_file_rank(
                            file=target_file,
                            rank=target_rank)

                    if target_sq == n_sq:
                        squares[target_sq] = 'you'

                    elif target_sq in effect_sq_set:

                        squares[target_sq] = f'{serial_effect_index:3}'
                        serial_effect_index += 1


            # ファイル出力
            f.write(DebugHelper.stringify_3characters_horizontal_board(squares))


########################################
# スクリプト実行時
########################################

if __name__ == '__main__':
    """スクリプト実行時"""

    Kifuwarabe.main(
            file_name="actual_55N.txt",
            # ５五桂
            n_sq=BoardHelper.jsa_to_sq(55))

    Kifuwarabe.main(
            file_name="actual_97N.txt",
            # ９七桂
            n_sq=BoardHelper.jsa_to_sq(97))
