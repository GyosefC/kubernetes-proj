import json

html = '''
<!DOCTYPE html>
<html lang="en" style="height: 100%;">
  <head>

  	<!-- Meta yo -->
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="favicon.ico" rel="icon" type="image/x-icon" />

    <title>Meaningless Video</title>
    <style>
        @-webkit-keyframes rotating {
            from{
                -webkit-transform: rotate(0deg);
            }
            to{
                -webkit-transform: rotate(360deg);
            }
        }
        .rotating {
            -webkit-animation: rotating 3s linear infinite;
        }
        .refresh {
            text-align: center;
            display: inline-block;
            position: absolute;
            top: 15px;
            right: 15px;
            height: 60px;
            line-height: 60px;
            width: 60px;
            font-size: 40px;
            border-radius: 30px;
            background-color: #3F51B5;
            transform: rotate(90deg);
            cursor: pointer;
            color: white;
        }
    </style>
</head>

<body style="height: 100%;">
	<iframe id="video" 
        allowfullscreen="allowfullscreen"
        mozallowfullscreen="mozallowfullscreen" 
        msallowfullscreen="msallowfullscreen" 
        oallowfullscreen="oallowfullscreen" 
        webkitallowfullscreen="webkitallowfullscreen"
        width="100%" height="100%"> </iframe>

    <span class="refresh rotating" onclick="updateSrc()">↻</span>
    <script>
        
    var srcs = [
        "VAC-5BQnuXI", "-w-58hQ9dLk", "ymFDtbk2teE", "oQaasxr3zWY", "NHO84rOp8FQ", "unSEV4v3qJI",
        "9ZS0diVzjxg", "pfwOqlnCKQs", "nPtMHSYtPc4", "RVP67Kffh3M", "Kpi5UXuoCzQ", "nLvhMOLKb-o",
        "IY9YNF5MMQo", "ihpG_NJ_T1g", "BENe8j_jtzU", "rY8DSFZ08JQ", "W1fPM0KRcRc", "RP5GqI4Jukc",
        "b3_lVSrPB6w", "XLV0b8KMAww", "XeDM1ZjMK50", "MmC4w0TAcLE", "wItgAhLaOrs", "a0uQnWAmf-k",
        "Uy5rz1cft5w", "FPF2e9_nPig", "N2an7F0KvUc", "DGCCMPXCNk0", "iRtu8FgYIAU", "3H3odKtfrTo",
        "nDbFSXNG5eU", "1mc-3mXrNaE", "Ul7IE3CTmSs", "szUJSXBjpJM", "4lKYYFVBeB0", "FahK9srJq10",
        "sXCFaJgpg1Y", "zYjcwYrq0VM", "8HlqSrCazqo", "8-Y0h5tATCI", "AF0jvXVaoOI", "u2-ZGCoKh-I",
        "Ju1M-SQLBro", "0uZX60akANU", "JHvrxWkz0Q0", "bSJAwndDTds", "S0xNNI9P4GA", "qGXzT1FdJsk",
        "qMlfBMP5Uo8", "iZjP_IoxCHU", "edHgxmiQYgc", "_03QSlEGLec", "HrN-GPYlcbQ", "vuw1mN_PUpI",
        "tvmlmcmLPQI", "1X6OAucemtE", "J15JgS7mu3A", "FGoOweTRht4", "pbhoBnbnzdk", "ZWOkZ_c8vxk",
        "MalLny7MT6E", "XkHdgMOuuBs", "avMOYdvf03E", "z5DqB0cv8uw", "_Fo0YBmsWAA", "Bu0bpgPA-eQ",
        "HeIkk6Yo0s8", "0t0uCWjQ6Og", "oaJYg8CMuJE", "vOPDD-2rjf4", "GEM3TNsxIQw", "I482t6JhL4g",
        "S6qLj8X67HA", "tT55pvSe9R4", "OvmvxAcT_Yc", "Bads-B8O0lI", "a_SF2p59aDY", "DqVonexxNBU",
        "tBQGHgIp7wc", "n-0C32d_q5w", "_xyGvpLOZ1Q", "Z0MbcACY1FI", "T8MS5C0C8i8", "BaQItKQdO-g",
        "wqTpHhaKtL8", "-m2fVWj99x4", "84WpcmJ28Yg", "uu-EuNeiTRE", "4zRWflXiWk4", "jgnG2wvykSE",
        "n0KVS4bMASY", "g1Og5Tg_Jyo", "1lkkG7_B4nE", "7YC2gcSHXaU", "YJj2jf0HTPg", "Vh473k-uHH0",
        "DD2SJqKfqZE", "RsM2ZbQtulM", "NOmMEmafvtA", "NiASF6-j3Vg", "qz0KKzvwWZc", "MLrNGIbqn0w",
        "ekGDWdyrvyA", "FbwX_POWAik", "V-fRuoMIfpw", "kJjEYZaX3V4", "daXZP8cvBG4", "rWNTvDgQv90",
        "5aWuqFU8doE", "U6DEJXFmQRk", "Ei2I3_nehOw", "KiuO_Z2_AD4", "eO63Ih0UAWE", "OCHCTW6ywUI",
        "e79SuHotazs", "X_UDguQ420I", "PkOcm_XaWrw", "ZvP08WpFk-s", "PS3jlUPPf5U", "ZzWqfJFxC0w",
        "LkCNJRfSZBU", "gPuI_pbCYOI", "M5rpbCQlo6Q", "FY8SwIvxj8o", "NWD7iqtOJSE", "3pHsZCml3fs",
        "Ur69gng_8zk", "lmpLZalaaGU", "SfA_L_zfqiU", "XYYo3T6nCw8", "sBmfKv-IPYs", "gwDkt4NkJkA",
        "TCm9788Tb5g", "TnmDFMrByOs", "ZPvgEGnHZBI", "dZQOsYooyDY", "5b15BAUxpPQ", "uGgI6qsg_kc",
        "Eht-kEzq88w", "zSWUWPx2VeQ", "uA-FoUIVedg", "FzjtPtOH-Hg", "-xOMiSSJ9Rk", "9hPS8-g3X7g",
        "ECceiU32vGs", "MExnipWnuDA", "yt0TqJS0gj4", "vJmJUallrYA", "4geLMAgamVY", "P6x6NO-Vfjw",
        "ZwipCJoWpsQ", "H8gKmQ6Hrro", "ZZbIx7xy5mc", "eyd51lvu3xw", "rtChPB6NjJY", "apm7b3rhPKU",
        "KhpRFURlwJI", "hBxJKT7YpLM", "V_MD8IVp53E", "i9TsmU9-e3E", "ms5a_C7EeNk", "pdQiSGb4Luw",
        "-Gq68u-f6X0", "4MWN48V0Oac", "rmZ_UVZWBmE", "cRpdIrq7Rbo", "YewU7gI5KDw", "Wwx1PqcmGHo",
        "zfHuoVAJ_vk", "OlKGfv-os1Y", "7YC7cVIeDHQ", "yhHCkiI__1E", "VCv90-w9YB4", "Nwij51EfgWE",
        "PLhWKzB__Po", "jxdcgCLyHPM", "riFvvig8ou0", "frDamZjCbkI", "eO696B03l48", "kNrxUVe4T1U",
        "3rYLLfAKtrE", "eq-9jmF1JYA", "iJskY0GyfTU", "DzL98O2MSRQ", "UMWW92UhpZs", "8QxbC495zdQ",
        "LlLGlx3NoLY", "Bxc_55ur-J4", "boH9-zDsL3A", "On7OMQGXVyw", "IYdWZ9XX19E", "UjSjVt81REo", "xO9FHt5_ohk",
        "kH24GXEDHxI", "HhPC8W769HY", "6DeBfvPiFN0", "tkNT28g6YBU", "SMQIkeINACY", "4PDHnVkxKI8", "8PpXAPanaDU", "SN0U8_mIVwc", "xFV9v5m1VNo", "Bfv6MqUfKzc", "4n0eYeosB7g", "xb8G8qA9ibI", "gFRylztSXvE", "vcOTiTVuizU", "4Q0diR34tSA", "RGKPfzBXzew", "x-tnUZMZoaA", "b3Qlu-vXMZg", "Dv9uZthgsRA", "4ZRLF6L-1bM",
        "aKn0HddzuWM", "w_je_Sx2ULg", "u0GSXxNh4AM", "E9VYHgjhQSw", "V2LU-lC-WX0", "NRNBTNENIfM", "_HloVUMR5Fw", "QOQLGzFEzI0", "KywJ7G8bNHk", "eLS__OeYnlQ", "7Uhkkg8ULbI", "1SUlMpg1apY", "pVD53JffuTI", "qOOSeqUzdlU", "TsqUOx5t6DU", "B-NllEIfMug", "zhrymM8vr0Y", "M0ZpV7ksHIM", "P0VF8xiF9vI", "fVvjuUcYG_M",
        "wuM3wrIFan4", "w8v-IifCPH4", "J6UYQVE1zAI", "hItgRaJjyPE", "dkVu5B-eLbY", "fQY-V0l2g5c", "q1ywTBzLFuQ", "KtpHdo69vKQ", "p_tilYlhSj4", "OpKOm-LLRhA", "SIhBc0cl3r4", "zneUKi29Kps", "wZLNggsTcHg", "sasdCg4da4o", "4ygG4t7SlYM", "9Pq9pRuO8ds", "A1MkBNoCnfc", "P2P_geamYPI", "Tu4Dq8NPLzU", "imnveG5YOVI",
        "YhwMAkw2Wbc", "3IV0eFxGEmo", "o30fv6wHp_4", "f7uTo3x8-uY", "Vv46fUzMbBE", "aSbs2gPdGSo", "zGBgTCc2X3E", "UJdOKKIrlEA", "7nOWBS1WoS0", "L9tuVtKJVJs", "7M9sejx8M30", "QLyXH4YaiCc", "S0HzNwTHJi0", "zcaAC_ElwnE", "UJwVCcoZ9PA", "4xSRbO7YLKQ", "vBJbMKj9UNw", "jBy_BjMUZfQ", "xHtSs9yUBfY", "uX6oNcLdnUY",
        "eEBQktyw-sM", "enYA4rLE3g8", "p1HYlomlb8U", "M-521H6b6us", "Gf8_40bYVGs", "M0D_br-HIsE", "GxhikfTsAps", "Zsr5G02H85I", "Rxi23dcIdHA", "VaqONei9ra8", "inEwzSjJIDM", "xGyWuRcHaJI", "tP_BdQeyEQU", "_rwm2m9Lfgw", "JA8beIzbzjk", "ku4SxHvnWwY", "vIiPn_I6IYo", "dF_zXozzmXg", "0SL_W-83AW4", "GTZ3-Eoj_DI",
        "INN82ox9iZo", "CcC-RPq388g", "E58zRsgaC4w", "C0dI-shH4sQ", "AKymadaASpk", "5H9VUjcvnY8", "8ZeWZdmKp1E", "oReVsLpLV0Y", "hFz_H8n1_Oo", "BgRuNlDNIOI", "HL1bOLu1AtU", "d_y07CpYCfI", "PASkasT5eO8", "RoOpe9vXnu0", "ZeQd_GzIz1M", "BKEL4cUTOI4", "dO-WmToIL7M", "XVaKk9nho6Q", "E9HiCAEKxXY", "DDKHN20zF-8",
        "meJNc4RuTsg", "_apRkJ6Gj0E", "Au4tlMRI1eg", "o5mLafiz96A", "HP66dH1yEZo", "-EbzDqtZEh4", "UG4Eg5KoGik", "nPmdTwU6XUM", "DqYm6kwSS_Q", "_7UNcbnwAZw", "2gmQYBZPV7g", "EIRilNVihw8", "4acESMXmjio", "avAncUsRTz8", "SR6FKTA2o2Q", "6cAyrdoVpZc", "MeCg9HIw2gU", "CbAat-Zixw4", "HB3XJEsCKtk", "1XjeyjQkLmY",
        "fsvCC2qPM4s", "AmQM5hKVryE", "hnvnhCeZZ34", "8oj3oI_Mr50", "vdYs_voapX0", "iFZMhe1WeCQ", "eEa0RJe-eG8", "OyDm_BOKBAM", "gg7HDYBn9Lc", "ox1IFSQV0k4", "LVyr4iR2wU0", "D6zsJOq_sYo", "j5PHO-v4RJE", "r0Hkq3ST_4U", "rGl9uq1YnGY", "L2z_pd69gAc", "cNIiYVO75mw", "9iym331fPek", "APu2i0rg7Og", "lkCCyi03KLc",
        "oaDALQN1jHY", "5iIkoB8B4YI", "z1KtTt7Ns50", "UHIB18POa8Q", "mdhXXw_0Lbo", "I3EuAWUgIGg", "egmwhCBklME", "VsDxGOfr800", "x9y_-66thPU", "A_QHVDMW02M", "jEOjavnc3VE", "IwQfjO8MUvk", "1f4Dxr-zvmQ", "xf-b3BorM4E", "nJl4FXkDwnQ", "-kmcRWhE0Rw", "y8qh7-4FPfU", "rfxVYZyWThI", "KjkzHGRR2LQ", "iRJ-WOCxBM8",
        "rUeTlk2F8DI", "_nim1EKaDAY", "UIBsVX_sBUs", "SFmM5CWnmtE", "rlVKVGShx84", "bULmuDafMYM", "3MXCW6otqt8", "ccgkxP-4tVE", "lHYC3pqwE6o", "QK7oacKDt88", "Hygj2wRODCE", "UHmTBBFNXbQ", "E8-8gJGT__4", "QLp5jNWxmpk", "BGaMHq6d3qg", "HrhKRB3QhxY", "aaGik_GLNbA", "SMrIrgysJfU", "L22keLHfEjc", "r4fKHiL8nIw",
        "4wvmkF5YNEE", "WHbRCYHq3Lk", "ZyWcr17feeI", "F7MlUH3q1aM", "meplQxAvRfg", "FNuNWDjZfYM", "Cren6zIhXAM", "oDmJtfejeRk", "Wk42sou6tOY", "PDUA8sb4-UU", "aCfrD6EwHfY", "jO5IaAKTKsQ", "nM8tPbI8Es8", "htKe_bXZ3JQ", "m-MYrBu88mk", "b5ynU4_u6Qo", "ZVlYbPK9ycg", "Tv5QlQj39XU", "3xJgVHcdce4", "TYxbDHGDTUQ",
        "AcmaNJfRQf0", "N7AuskKrW7A", "zaKyglWb6Rc", "m-xQJTvXjGE", "OyBmEeojfKo", "c5B73kPjf0c", "otq2x0Cz6C4", "_J9RH1mCqpk", "z7pgNXaz804", "8qtevHY7rl4", "ZwIQvGl7LPo", "m-U7maWWB0w", "dRR_pXJT0zU", "4F0Mer4kDDY", "HphwQNhByOk", "ixlurWilkt8", "3l2htBOnAtM", "S6U-_ngi6-o", "8Fm7tB1vIKg", "SWSHWP1e6Ns",
        "NZOFukA2V0A", "ggJueBSS_P0", "UkRoCE8J0Mc", "QV4sVAK-5GY", "pCNJ9jnTjAA", "Mb399Xdplyk", "Jm0YHqYqjxo", "v4kaNXX7KLs", "05h83_OsM8s", "dU6bGLA4Sv0", "sox0peW7ZRg", "oJ5Q8I4U9gQ", "IUGjzpwNtjE", "8DZAqou_zgI", "jTsb1kuXOx0", "Sb-v9YL4XyU", "Z-O5_YB0uiM", "m8aaoC2hrlc", "yswygoE7QC4", "in4Lju4kLEg",
        "caG8YQZlbAg", "IasEnrxangg", "wwOipTXvNNo", "D6qga9eoAxQ", "AXxBhOc7jEA", "5QiANaRWeWo", "3yMy7JuGpJM", "6qNOIJNfICI", "dI2Hw1_xy_g", "6pcTYdZVWtE", "izREDpUHIqQ", "bQCHHGtc0Fs", "72M3E9HlzBY", "MgTVrcRUMig", "KTcIrIGAoBc", "LbfvR5JOts8", "oJ4S1QertFA", "XNpruszbLPU", "CqrO2_LDhxk", "78PbcaA-QjA",
        "l9glG3yxNWE", "tf6uAsrROhs", "264Ixp43dZ0", "zPK382eJIns", "bZ9-PFes3mM", "dLSYsTtL2pY", "AkW-EAkClbE", "jWVqImbn67w", "K6yXoPyGcbg", "VSs_VmWNLys", "Qn5diT7Gkas", "zGbUhM7sJYY", "2CoSLzgjgAc", "HD4Ek6Q9i8c", "euoT7AEqn54", "jjnIxNH3thg", "C9es4KJmG34", "DcYlq7-hf70", "9fTiy5CU2TA", "gNeRdwwuJzY",
        "_jeWKmS5mT4", "_wH_ZL2lm40", "E0cZY7ef_mk", "oGxq-c5ihSo", "_sF6JkjpGtc", "X6qkAmaYMag", "cSZBae5xou8", "g1nSPZt2TvY", "NgXI48tDiWc", "VakD9DPWegM", "7I8HJNNUglo", "82BBA11mp70", "dIkO1eWFbuo", "-0DQ1Fv8Ej4", "IKYHhA8XvLw", "FRIaKMdO-Vw", "3hkM8BuPNuE", "gI8FxHemty4", "bZqqKb6H9n8", "bLHL75H_VEM",
        "oaqNCMudjOc", "Ufyxbzhu-rU", "s-EEjV_BJyQ", "oO22bjqxsz0", "9RV9Vb3IRpw", "9oYs_hSlfy0", "ih3Y7YRyVY8", "o-oPpQVFW18", "Zp4DDdbfBVg", "PxTjREYM060", "MN-CTB_SqCs", "fPEhhS26vb0", "c2KfmFzCe9k", "uF5ivqakjIc", "ywKu9DSESBQ", "NLkDLy2TYxQ", "qoLS9We9hl4", "5r3kUROGAOY", "StrDCAqpEEs", "IPnTH-cCRE8",
        "mxyPtMON4IM", "JY9UquC-6vU", "IdtKbq3Omkw", "PZ0KAUCBN7E", "9UnLkMbc6-Y", "tWjfbUfcJUM", "TddPNLQxk0Y", "86PUB4u2s2A", "sMCKBiChtiA", "4nu9ugMJ5L8", "1lgDiAInFLY", "pLJegq01S6A", "1s6aNjJRbrA", "nvHIGxs6JK4", "IIL5klObiQ4", "LK3O4faPbnQ", "gbt61vcAkG0", "vYgOpZn1-qM", "TDJ5cFM_YMw", "xRkfMqpXKuI",
        "QnZ0cKLWYWU", "tOsck7jYUsE", "Qc6AHtM8qKM", "nrS7HaAZQro", "U2iEPS4vMQk", "TDa2vKmHZ9c", "qmcSgoNb-1w", "1WTvl4gOyTA", "9WrAs1r_w8g", "mZpa3nOLOa8", "J_2nY1KpEJ8", "pCYEt7klfgQ", "xb0yMXrsKkI", "hPFbo8PXIOk", "zQufTfdHMfI", "HPjJCVylFBo", "IrszAQuTgc0", "WZP4Nu_8Ark", "kZSfPPJ4Fk8", "AAj4_1PLLL0"
    ]
    function updateSrc() {
        var randomId = srcs[Math.floor(Math.random() * srcs.length)];
        document.getElementById('video').src = 'https://www.youtube.com/embed/' + randomId;
    }

    updateSrc()
    </script>
</body>
</html>
'''

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html
    }