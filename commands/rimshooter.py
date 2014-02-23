#!/usr/bin/env python
import zlib
import random

#data taken from http://en.wikipedia.org/wiki/List_of_birds_by_common_name
data = 'x\xdau\\\xbbv#=r\xce\xf9\x14\xcc\xbc\x1b\xf0!$\xea6#i\xc4\x15\xb5#{3\xb0\t\x92\xf8\xd9l\xf0Gw\x8b\xc3\x89\xfc\x02\x8e6q\xea\xe3\xd0\x8f`g\xbbN\xfc\x18~\x12\x7fuC\xa3\xa9\xf19sF]\x85K\xa3\x81B\xd5W\x85\x02ok\xbfuM7\x9d\'\xdfv~=}\x0b\x8d;\xc4~\xf2\x14\xba\xae\xf6\x99\\\xd6\xae;\xcfV\xc9\xbbQ\xad\xb7]\xa8\xf6\xbe\xcb\xf4=*\x0c\xd4|\x17j\xef\x9a\x81\x0e\x8dO>\xf6m\xe6\\\xa7x\x1a\xca_\xda.\x85j\'\xbd\xf84}\xddy7Y\xc6\xbe\xdb\xf9\xd4L\xe7\xaem\xe3\xc9\xa5\xf3\xe4\x06\xffo\n\xfa\xf6\xd0O\xbe\xc5\xd4\xed\xa6_\xda\xda5\xeb\xa9t\xfb\x18N\xc1\xbecy\x8c\x1d\r\x9cyW=^\xe4\xea\x80\xa1]\xa7\xbe\xdd\xcd\xba>\xed\xfdy\xf2\xec\xea\xda\xfbM<\xd5\xf4\xe8\xe3dQ\xbb\x80\x17\xef\\\xb5s\xb5\xab\xdc\xe4\x9f|]\xc7\xd3l\xdf\xc4\xd5\n\xbd\xcd\xfb\xc4\x83\x98<\xc4\xd4\x80\xbe\xef]3\xb1\x99d\xe2\xa6o\xf7\xe7\x19\xe6xk\x9c\x07_\x1f\xbc\x94c:\x1c\xbf\xed{_c\x08 K\xe6\x1c#\xdc\xa0\xdf\xe0\xa6\x7f\xea]\xa8\'\xd7qu\xda\x85\xce+\xf9\x1ej,\x84\x8c\xfc\xb5\xdfl\xa8\xcb\x84\xc9\xf5\x93\xe7\xd8t\xfeg\x7f\xb0\x86\xcbc\xea+o\xa5\x0f\xee\xa7\xaf\x8d\x98\xbb\xa3O\x15*\xd5\xc1O\x96n\xebg[)x\x8d\xd5~\xba\xe8\\:\x04\xc8\x07\xbd\x0c\x1f\x9e\xbb\x08\x07\xcc\xc7\x19\xf3\xb7l\xe2\xa9BU\xacu\xbfwi\xbap\tk\xb8\xdeJ\xcf\xd3\xbb\xe4\x9a*\xd6\xa1\xa15=\x17\xa5_\xfbf\x8be\xb9\xc6\xec\xeb \xe7\xf1p\x88\x8d\x11:\x87\xef1\xaeg\xc7\xdc\xea\x01\xa3(:\xb9\xae\xcf\xdd\xee\x1f M\xc9m\xe3\x11\xa3\\BH\xd3@\xbe\xf9\xc3!4\xd5\xbe\xacr]\xa3\xcb\xe9\x02\x92\xd5B\xec\x8b/\xc1\xa4\xb9Z\x05\xf8*m\xfbv\xf2\x8a\x01\xc88y=P\xe4\x9b\x921\xf7\xe7:\x8e9\xbc\x1d\x1a\xfb\x96\xfc\x96[Lo\xec0\x8c\xcc\xb9\x8f\xf5\xda\x175\xbe4k\x12\xc7\x85\xae\xfd\x02\x83:\tM\xb3;;Z\xbdyl\xb61W\xcb{cYa\xdc\x07\x9fL\x103\xfd\xec\xb6\xc7\x80E\x8d\x11\xcb\xb6\xa4.\xef\xf9\xf1\x9d\x04i\xb6q\x15M\xf2.\xb4\x1d\xd6h;\xbd\xe9\xb1\x92\xb6\xfb\xb4J"aZk3Z\xc5\xdam\x95\xbavi\x86\x81\xads1I\x83>>`\xfc!\xe4\xf7\xcd]\xe3\xd6\xce\xda%\x0f\x8d\x93\xfbh\\\x05Q\xf8E\xbd\xb9\xab\xf6<.!\xb1\x1e\x83\x06\xfa\xe5[\xbe\xfd\xfd\xaf\xcd\xdf\xff:k\xfa\x80uF\xe3)}\xf1\xe4\xb9\xc7\x9e\xe1\xa7\xf7]\x8c\x90w!\xde\xfaf\x9d\x9cV\x81\xe4\xd7P\x1d\xa1\x9a\xde\xd5a\xbb\x83\xcah\xdb\xe9\xb2\xe3I\x94iY\x1e\xfb4;a4\xf9\xe5\xb7\xdb\xf3\xb1\x1b^~]\xf7^\xaa\xbe`+\xc7**\xff\xaaY\xfb\\\xe9j\x03\rG\x0b{\xde\x1e\xce\xf6\x99"-\xcb\x9d\xaf\xd7\xd4|\x11\x9a\xfd\xcc\xbb\x84\x17qw\xcf}[\xc5\x8f\xb3\x10\xb4#\x94\rM\xe7\xf0&]5\xb7>A}M\xae0`~\xc3{\xd8\xfa\xd8\xb0Nsi-\xfa\x91Ee\x17?|\r\xd1P\xdd\xeb!\xf5\xb9\x10\xaf\xee\x8a\xcd\xc8\x85\xcf.\xadj\x1b\x8bIv\x84FD\xafo\xfd\xa6\xb3"\x93\x9be\xe5\xfa\xe3\xe4\x91\xd6\xed6\xacI&]\xaa\xfd\xef\xbd\x8dTW\xa6\x8a\xa8<y\x82<\xcf\xe8\x95\x17/\x90\xfd\xe1\xcf\x90\xa9\x83?\x19\xf7\xd9\'(\xa3\x96\x06O\x9d\x98\xf0q\xc3\xd7~\xbd>\xe7\t\xdb\xcb\xd3\xed\x01\xcb\x1d\xa1\x96|\xb3\xc5\x00dTF\xdcC\nc\xcc\xe4\xd5\xdaC\tf\x92\x14\xe0.\x1eI\\\x8e\xcaz\x86\t\xc0v\x08\xb9\x8e\x9a\x03\x0cs\x9dyjpr\xaf\xb6\xe0\xb9\x8f,iy\x1c\xae\xfe\xdb\xbf\x1d\xa1\x9f\xda\x81%j\xa8\xd7\xd9\x9au\xbb\x14\x1d\xcft\xf8\xc0\xd7\xd3N\xb8`I\x8b\xbc\x90\xc2\\\xc6\xd8\x9d\xa7W\xf5\xcau)\xb6\xadv\xb6\xc2\xc2\xa3\xdd\xc0~rg(\x97\x82\xf1\x1a\xcf\xae\x1e\xe8\xe9\x1f\xd6\xa1u\x87U\xd8\xf6\xae\x0b\xb1\xf9\xe3\xe4\x1d\xb2\x079\xc3d\x0e\x8d\xb22\xba\x0f\x04(\x16\xbeK\x1e\xf2\x08\x81JU\xc7\x9f\xcb\x8c<\xc4\xbb\xbe>\xb8$:C\xcb\xee\\H\xb0\x12\t\xef\xc0\x92GR\xdc\x9f\xbb\xe1\xd2k\x9f\x0e=\x14\x85\x16\xb3\xb1\xb1\xe7\x98\xceh\x88\xed\xe4\xd2\x89$R\xa7\xa1d\xec0\x08\x13\xbb\x82\x8f-\xf5\xa3\xa4a\xf5\xda\xd8Pg]L\x87\xd9Q^p\xdb\'h\x112~%WE\x14\x13\x8fi1\xa6N\xb8\'\xf3\xba\x1e\xd7\xbfjw\xe71\xe7\t\xca~w\xf92\x15\',\xef\xca\x1bpq-k\x1df\x89\x96\xeed\x1f\n\xeb!\x02\x14e\xc5\xcc\xac9t\x00\xcd\xa6P"+\x19\xa7\x0c<\xc8\xfa]\xed`3\xb7\x11\xa3i\xdb\x92V5\x96i\x03w\x99\xc1\x9a\x89\xc6\xbe\xcfB\xff\x82\x9d\xb3"\x9b-l\xdd.\xc4\xf1Vu\xe9\xd6\xeb\xda\x8fy\xfcM\xfa\xfc\xd5\xadB\xeaI\t\xb9U\xec\x95i\x83\xbdZ\xff\xd6wd\x16\x0bD\'\x8d\xbf\xacB;\xa0\x08\x9e#R&\xb2\x1eb\xf6\xb8\n\x94\x15\x94S\'\xc4}\r9>\xcb\xf3-A;\xea\x0f\xc81\xf2G`W\xb4\xf4\xda\x82#\x1dW\xfa\x9ak,\x15\x04{hj\x0c\xa03\xdfVd\xf3\xde\xa0\x94\xc9fB\x8b\xd8\xcaZ\xa5k\xecf\x9b\x86\x07\xae \x83\xadHM\x83\xf7\x8d\xcc\x92\x96\x08\x14\x91\xe7\xe5\xef\xbd\xab`l\x84\x9a;\xee\xf4v\x9b|\'\x98K[\x00\x849\x00\xe4\xdc\x1e\x02\xc0\x06K;\x01\xa2be\xf2P\x0eMza\xb3+\xe3z\x83\xe0\x87\n\x0b\xb26\xb9\x93-T\xf0\xa5\xeb\xbb\x04\xd4\xd8y\xe6\xccw\t\xf8\xe2\xe0ZC\xe7e\xe1\x83;\xc0`\xed\xe3Q\x1b\xca\xea-\xa0\x89+\xc2s\xbb\xe8y\xa2\x8b\xf5\xb521_F\rfo\xd4AV6\xf7\xaei|w\xb1\x81\x84\xf7\xec\xda=\xad^\x8c\xab3\x1b\xf1\xd9\x06\xfa"s\x16>\xf5\x1f\xbc\x9aB\xb2\xe1\x86\x8e9\xc4D\x92W\xc0\x85\x81y\x13{\x98\xcc,\x18C\xc1\xa0:vn;!\x7f\xc0\x95\x9d\xe9\xc6\xcc\xf4U\xb3\xc3\xd6r\x93/d\xc6\x02T27\x13\xcc?\x15\xa7\xc1\x8bM3B\x8c\xabQ\x85\x0b\x01\xe0\xb8\x8e\xc9v\xb1Ryz\xe6\xd8^\xd8\tn\x8cO\xb0Q\xea*f8\xfb\x88\xaf!\x95\xa4\xdbX\x15Ln\xfa\xe4\xfa-\rwz\'\xadl\x93Z3\x18o\x80\xb9\xe9\x1fh\xdd\xff8,\x98\x15\xe7]\xf3\x00\xdf\xea\x8c\xde\xb08)\xf7uN:\x96E\x82\x8d\x80\x99\xd6\x02\xac\x8e\xdf\xb2\xe7\xa4\x8c\xa5\xc7\xac\xc3V\x9c\xb1\xb1 _/\xed\x11\x9b`\x98\xf7\x87\x08P\x01\xb7\xe3\xe7O\x82/K\x82L\xf8\x14\x15\xe3G\x88\x0e\xec\x11\x08y|\x0emK\xff\x8e\xc7 \x8cW\xab4\x92\xfe[\x07\xfc\xaf3\xcf\xa5\xd7\xc9\xed\xa0\x13\xcfB\xd9\x94\xde\x05\xf8:Z\xd7\xd5\xd6\x0cH\xff\x00\xc0\xda\r+\x08\xebC\xf3j4@(\xf6^"\xbb\xe0\x9d6\xca\xc8\xd3*\xc9xV\x18A\xd1R}\n#\xefS\xd8l\xe2@\xbf\xfe\xed\xbf\x80n\xea\x1a=\x1b\xeb\xc9\x81\xd3\xa9~\x1c\x89\xd4\xac\xda\x89,cz\xf6\xd0\xa5<\x0c\xd3\xafK\x9f\x8e\xa4\xdddp\xef\xc4\x84LAe\xe3\x83\x01\xfe\xb0\\\x00l\x90\x85\xda\xf7\t\xe8\x96\xd4\x8crmn\x94\x9e\x01\xcf\xef\xe1!g\x064\x11-\xd4\xb0`\xea\xc6[1k\xb8\xfb\xd8\xee\xa8\xdd\rl\x1c9\xebM\'>\x83ps\x00\x00M\xe2\x89Y\xd7\xbe\x85\xbc\x16\x1a~(\x9a\xb3\x83\x80)\xe1\x91\x0c\xeaC;\xbb\'\x7f_Q\xa1\x8di\x8e\xad\xea\xa5\xfe\xa2\xee\x0f+\x0ep<Hg\xbcoD2\x98\xb3t\x1f\x90k\'\x84\xa8*\xf9d\xfa\x9e\xd6^\xab3\x1e\t\xb9\xf3\xc7RK(p\x16k\x99dR\xca\x18H\x0f\x94<T\x81/\xd4\x08^a\xba\xc0\x95L\xff\x05\xb2o2\xcb\x0c\x86\x91\x05m\xe3\xd5\x0f\xbb\xf3)\xf5[\xb82\xf6=\x0c\xd65\x96a\x950\xf2\xa3\rj\x01H@\x9b\x05\xd3q;\x12\x90r\x87\xc8sv\x16tAU\xae\x9d\x88N\xd6wZY\x9ce\x13/\xb8\xfe\xe3\xad\xf7\x1d\x03\xf5\xae\xff\x81\x0f\xd7:nW\xaf\xe0+d\x86\xcc(\x8c\xcf\xec\x94\']\x85\x18b\xda\r\xaf*>\xa1\xa83W\x1b\\\x8c\x9dB\x17\x1dM\xc0cL!\x13edIY\xb25\xe1\xfe\xb0\x055\xae\x19\x7f%\x1f`0\xa0C\x87N\xdd\xb6\x9f,\xfb\xd5\xda\x03\x83u\xf0{ZU?6\xfd\xd8r\xc1\x1f\x1c\xea\x00\x89\x08\x80\x80\xd9\x80"O\xd8\x9e\x93\x97}h\xe0\x19O_\xc9\x97\xfb\x1e\x12\x161(u\xddo6P\x14\r\xa9\x18f\xbcK\xa8\x8d\xcb(\x0e\xc4\xf2#\xdd,a\x85\xa6\x7f\xa8\xe8\xf9\x8f\x93E\x9f\x8e5\xfb\xd1\x87\xe3\xce\xc3}v{\xb7\xfb\xfb_\x07E\xae\x15 uP\xf3}\x9d\xfd\xda\xe7\x18\x135\xc8\xfb\r{,[\xdd\xbb\xd0\x90\xb5%5\xe8\xcd\xbb~K=\xd6\xbf+\xd4\x83\xd5z\n\x87#>\x8d\xbez\xcb\xa8UMQ\x96\xc9\xae\x8b\xcd\xef\x1cA\xa2\xb92\xe8\xc4;\x14\xca\r\xea\xa1\xac\xc2\xcac>\xaa\xb3t\xa9o\xed9\xacH\x08\x1b%\x817j\x98\xe2%\xa6nG\x90V\xb8\xfa\x8dBpx\x81t\x8fv\x807y\x8a\x11\xd6\xf0`\xaf\t\xdcO\x995\xab\x84E\x9e\x8f\xb8%\xdd\x8eQN\xe9\x1b\xd6\x91\x1c\xb8<g/g\xda\x19\x95\xeb\xa0\x87\xd30\xe7\xb2\xa5\xc6\x85x\xf9\xca\xda\x8b\xdc\xeb\xbc.\xbbPw\x13B\xb7\xfc\xb6k\x11\x02\xe1\xb2V\xbe\xfa\x88\x95\x02\xbe\xc6\xb3)Q\x0ew\xd3\x1e\x02\x00$L\x04u7\xa8Fc\xe8\x82\x1a\x99\xbd\xc1\xcc(\xe2\'\xc6\xcb\x9fg\xe10\x19\xb5\xc4\n\xe59\x7f\xea\xb8\xca\xabt\xa4\xd4#\xac\x0fYW%\xbf4\x8c3oH\xb5\x10\xb4x\xc4\xe7\xae=\xf9s\xe9\xcc\x9fn\xdag\x01\x85)F-\x1c\x07C\xfd\x15x\xa6q\x13\x8b\xcd\x99\xaeQ\xb6\x9aZs\xe9\xbc_\xb7\xd2:#P\xf8A\x1c\x12\xfd\xcaq\x0e.\xb4\x10\x0f\x13\xe2}*\xa4\xbe\x89\xa7 \xeb\xf6\xd0\xaf\xa1\xbce6\xd6`rxM\xdf\xad\x9ca\x0b\x89\x04a,\x87\x15{\x89\xa4\x99\xb5G-\xd3Wb1a\xba\x9a\xc1g\x92-\x83\x1d\xd3\x16^\xfc\x1b\xbb\rir\xd37\x14\xac5\xadL\xc2~\xc4\x90\x13\x07\x98\'\xec\xf8dWm(#T\xd4\xc4\x91\xe0,(`N\x98k\xc0*\xb6\xa0\x05\x94O\x0e\xa6\x1av\x8e-\x85;\x90\xc9\x8b}b\xc4\xdc\'\n\xf3\xcc\xcd\x06\x16U\xc5\xe6\xf7uv\xb9\xf99O?<\x18\xfe$\xe6>\xfa\xfa(O\xe6\xf2\xb0?.8\x89\xf9\x19\xb52\xf5\xe5#&\xed|\x14ab\x0e\xfc?2\xd1\xfc|\x81\x1c\xe5\x15\xf8/{J\xac\x91]{\xa4\xefdB\xfaSM\x05`\xd8\x85\x13\xe9\xd8+\x89jp\x15s0\x99\x18"\x1eLJ\x0cc\xe8I\x1f\xd9\t\xfa\x16\xd7\xeb\xb3\xc2\tf\x7fi*W\xd6]\xee\x03\xb9Y\xa3h\xdbr\xdf\xeb\xe1\xcat\x111\xc9\xc2\xd0\xe1\xf0\xb3L\x99\xb0\xbb\x9a`\x15\xf4\x12\xe4`\x08rQ\x80\xea\x9e-\xdb\x81\x96\xdf\xfd\x8cIT\x0b\xbf\xb5(\xd9Q@\x14\xaeeKM\xe0og\x8bJR\xa4\'\x0eO\xa1\xdau\xbe\x81*\x0b\x1cr\x19J\x16\xa1\xc9\xa3\x1e\xb8\xcb#D\x8dx\x0b\x89t~uGh\xdd\xd6\xeb\xa1\x810\xe5\x18C\x9e\x0b\x03\xa4Ru\x03\x894)\xe2\xf0\x85\xd6\xa4\x08\xac=\xc3\xdb\xa2O\xe5\xaa\xdf\xdc\xc1\xc1v\x8c\xdaa\t\x9a\x9f^U\x1c\xec\xec\xc6\xff\xb0\xa67\xc1\xa1\x86\xbe\xe6\x19"\xddp\x90\x9d(^!~RW\x02\xa0\xc3\x06\xc4>\xa8\n\x1e\x1f\x87\xcc\xd6\xc4~\x84\xd8\x13\xb6.y\xdfB\x15Wt\xec"/\xfc\x1e\xaa\x0ep\xc4e\xab\xa6\xfc\xa7\xfe\'\xe3P(+\nNQ\x80\xab\xcb\xeaN\x82\tZ\xf3=\x1e\xb0\xc9\xe1\xa2\xf7\xa1\x93W\x90PfKZ\xf0\x9f\xdd\xdam]\x0b\xd7\x8f\x03\t6\xe1\xcb\x1e*aUV\x94\xfe\r\xd2Y\xbd\xb7x\xdcCg\xd8{\x1f\xa1\xa8\xd3\x7f\xff\xc7\xc5,=\x02c\x1c#\n\x1da\xbc\x06(\xed\xc15[\x8e\xe1\x12dg\xd8p\xc0rV{\xd7\xc5X\xe2Y\x91\xc0\\\x02W\x7f;\xdb:2\xcd\xc6R\x11\x06j"\x9b\x8bq\xd7\xc7\x1d,\xd4\xe0\xb3\xe7\xa6\xb5\xdbA\xb6C\xb3\x8a\xa7\xe9\x13\xa6w\xefI\x80\xb9<xF\x1a\xc4>O\xbe\xbb\x14\xe4Y\xaap\x18:S\x0bw\x84\xbb?\xd04i\xabH\x11\x08s\x89\xe7)\x1cZR\xd9\x98q\x1aR\ta\xf0\xbdN;\x05\n\xb1\xcf\xa7\x1a\x0c\x96\xd6\x99\xc3\xf2.\xcf\xd7=\x902\xc5Z$`\\\xb9cQ\x91\xd7l\xdc\x96Y\xf6\xc2WW\xfd\xde{1~\xdc\\M\xb7\xd6-\xb4\xf8c\xb1\x1e\xdcE\xe3\xca\x01\xf9-\xb9\x86J\xa9t\xd8\xea\xc1]2A\xcf\x1f\xc8\xf2\x96\xf2\xcb\x84I\xe7`;\xf5K\x9f \x19\x16j\xcaa\xce\x92\xc9f\xee;l\xb7\xbd\xe7\xb6\xaa}\xd5\x01\xd8\xd9\xe0\x07\xc9?\xe7q\x0e\xde\xb0\x8d\xf5\x18\xc8\xa3\xa0\xa0\xffI>\x8c\xfc\x873\x9bO\xe5Z\xf4P(\x16t\x9b\xa7\xa2\xd9\x88\xa3_\xa2\xa7j\xc3W\x8f\xfd\xb9\xa2\xf5\'\tx8\xbb\n\xb0eg\x95zr^u\rTF`y\xc9P+F\x19\xf8\xb1\xd9\x0f\x94bg`\x8f\x0f\x8c\xa6\xacW\x8eZ&\x83T\xf6\x12\xf2\xb3\x0b\xe9Bj\xa8d8\xbe.\xc5\xc0\xbe\xf1\xea\x00\xbb\x00c\x08\x0f\xa71\xa2Tq\xda\xc6\x86\xa3\x9f\xab\x15i^6\x04\x15\xa4\x92\x06\xd6\xf8\xc0\xe5.lgGa?D\xd7\xfd\x0c\x16\x17\x85\xc6vU\xd4\xed\xa3Y\r\xc2\x12\x17\xe5\x92{\x17Z\x02`tJ,\x0c\x8d*\xcc\xe0B\x9dgET\x93\x03\xa6\xd6U`\xa8U\xedc4C\xa9\xa0I\x99j\x1e\xd8\x8b\xacF,\xad\xa0\x01v\xa58\x11\xc1\x08\x13\xd0[\x18m\n\x15)\xfb!\xa6v\x03\x95\xb3\xc6P\xc5\xec\xe4\x97\xed(\\V\x0f\x10P\xbaak\xf7\x18\xa1\xa4\x96p@\xe1$\xd7y\xc8|F\x03\x985\xe0\\\xa2*gAm=$R\xde=\x04\xea#G\xe9\xaf\x9a@f\x1f\xce\xa1\xf66tQL\x08y\x95\xd1\xadSO\x81\xbcRa\xa8\xa7\xf0r\xaa\xf9\xf4\x97\x1f\xcc\xf3\xa7\x83k\x0fG\xe9\x85O\xb7\xf7q\xef\xe9\xa4\xf0\xd8J\xa5\x1c\xb1!\xd6lt\x02^\x1eh\xbf\x9c\x0c\xef\xe9q81.\x83\x04\xdc<\xf78\xb0\xc4+\xe3\xc1\xd5n\x1f\xda\x8e\x1db\n\xdeq\xf1\xc2\xd7J\x92%\x8d\xf9M,3\xd4\xea\xcd\x9d\x1ay\xfa3\xbe\x97\x1f,\x0c\xa2_\x9c\xf4\x91\x00LGg\xdfBf\x8f\x8aDf\xcc\x91h,\xbd\xac\x8c\xc9\x0c\\\x93\x97\xa1s\xecJ\x06{\xa7]\xc0d\x17L\xb1z<\x9b\xf5f\xfc\x96\xa5;\xa1>\xd4\x19\x8f3\xab\x95\x97r\x9a)\x08\x1e#\xf96\x07\'G<\'\xf5>\xe4\xc0\xfa\x85\x93\x17\xd8\xd2\xe5\xcf\x10\x7fg(\x1f\x16T\xe6\xea.\xc5\xed\x81^0y\t5o7\xdd\x1a\x8b\xd8\r\xbb\x86\xcf?8\x08W\x88\x12\x7f\xd4\xac\xa1\xa2\xdf`\xe6\x16\x0e\xeb\t\xb35\x1cS\xc7t"@:\xdf\xf5\xec\x07\x93~\xc7\x9fud\xdf\xe98\x03\xd6I\xcc\x86\xb7_\xef\xcf\x86\x1e\xbeY\x879n\x9c9\xea\x86fZ u\x02<(\xdb-;>\x9c\xcfV3\x17\\\xad\xcem\x1b\xd8\xcb\xcb<\x8e\xc0l\x1c\x1d\x93\x9d\xc2\x06\xd0\xc2}xy\xa4\x15\xbb]\x07Ry\r!\xbf\xccT\xd0hG\xc0\xdf\x00\xec\xc0\xe6p\x0e\x97\xa8\x8a.\xf8rn\xa1/\x80\xdbHap\xa1\xaej\x0ewi\x91:\xaaL\x8c\xa0\xe92\x10\xdafx\x0f\xb3W\x17o\x87\xc7u\x08\xdd\xc8\xb9P\xd6\x02^\x83\xab\xbbh\xf4\xf7\x10\xc9\\.\x1d\x9cVA\xccc7\xea\xa1\xa7\x84\x9d\xad\x1c\x1b)\x1a\x02Pt?\xe1\x7f\xae\xb0:\xf48\xaa$>%\xeb\xf3\xc9]R\xe5\x17\t\xb8P\xb8\xac\xdf`\x9b\x14\x88\xce\xf8\xc3\x81\xd6\xb2\x93<\x99N\x02e4:\xc3I\xe4\x0f4\xe7\xc3q78\xa1\x04\xda\x01&z\xb7\x8e\x1c\x18\xa2t$\x8a\xd7\x91niCv^Uk\xab\x8e-\x87\xbb<\xc5\x94\xdf]\x16\\\xac\xe7\xa8\x8d\xb99%S\x87j&\xf6\x9a>=\xe8\t\x92o8\x14\x02G\r\xce\xa6\xe5\x0f\xd89\x1d\xc1X\xda\x89ir\xed\xfd\xa8\xcb\x91ox\x06\x18\xd69\xff\xd5\x98\xae\x9a\xc6Q\x94\xb9\\\t\n\xfb\xadUp\xf2\x98\x9f\xc9S\xe3\xf2\x02\x19\x0e\xcco\x94\xbf\xe2\xe8\xf8p+\xb6\x9e \xc1\xf4\x0f\x94\x05\xf3\xc7\xcb\xcc\x87\\\xa9\x85\to\xd6\x04*\xff\x84\xf5\xfc\xe9H\x93I\x0e\xa3V\x11\xa4\xa1\x84\x99\xd072dt\xdc7\xa7\x83\x8c\xa67\x85t\xc5\xa7W\xe1\xc2\xc2\xe5\xdaw\xc1\xa7s\xb6{Z7\x0b\x841\xc8\xf4\x7fj\n\xe1\xefr\x87\xf8f\xca\xac\x81\x1f\xcb\xc5p\x7f\xaa\xa8U\xe1\xde\x0c\x96[Y\xa3T\'\xe5\xc9|\xb4\x8a2\xa0\xeaW<\xbe\x94O\xff\x955J\x0eQ\xde\x9c\x8f,$\x82\xa7,\xc5[&Bopy\x01\xcdy\xa9\xf4\x04J+^\x9cF\x14o)\xf0\xb0r\xcd\xf0\xf31\xdb\xb6\x0fk?\x98\xd8\xf7t\xa6\xe0\xd0\xe4\xa5\xdaa\xcc\xb9\xbfE\xa8zRi\x00\x14P\x16M\xa6e\xf7f\xf2\xaa\xa2\xf06mJ\x92-\xcd\x81Q\x04Yp/\xbe\xaa(\xb9\x0f\xb5\xfbE\xcd\x1c\xc8s\xc7\xb6\xcf\x1d\xe7\xb9\x1f\xd8\xdf\xfaUp\xa3\x11P2d3~\x07{\x00\x1a^*\xf8sLh \xf7\xb5\xe0\x89B\x1e7.PdQ\xf0\xc0Y1\x05\xe3&\x92\xd9,\x18y\x8e\xdf0\xb5\x90\x87\xf8\xcbIQHW\xbe\x92\x8d\xd9,\xd6\xe1\xc3\x97\xfc!G\xa7\x0e\xfa\x01\x87c\x1c(\xddBe\x93\'\xca[\xbd\x18\xb88\xe1\x97\x9f\x98c\x90\xa4\r\xc6Q\x9b\xe1s\xc4\xea\n\x9e\xbf\xec\xd1\xac\x1be\x9ex\x9a\xec\xc9K\x82k\xef\x7f1\xf1:\xa7\x94\xbc\xfc\xabq\x0c=\xa8\xad(B\xbd\x94\x9b\x04\xa5E\xb8\xcf\xa4\xc9\xd8\xd2\xabQ\xa2\xbb-\xee\t\xb5\xab\xfa\x8e3M\xb4\xe57:\xa6\xc9z^4O\xae\xfa\n<S\xe4V\xa3.\xbb[j\x1a\xd9N\xbe\x06(\xf3\x83\x1bN\xcf\r\xf0a\x9b\xaf-\xa4\xedK\xbaT\xe7\x03\x17(\x07\xf6rx\xd7P\xf2\xdd\xa3\xa4\x9b\xc2e\xe8\xce\x19\x05\xc8\xa8g\x8e\x99\xbc/\xcc\xa5\x04\x8ct&\xee\xd6\x990G\xce#s\xbe\xc5\xd0\x9e\xf5\xd9\xf2\\\x99(\xe2z\xcf\xd8\xfbt\xb2\x93\xb3\xa3\x8dA\xa7\x14\x97\x95\xd8\x0f3\x02"O)\xdcu`WaGg\xdc\t\x16\xf0bE\t\x89tUO\x07\x02\x06\xc19D\xe55\x1f\xcc\xa5\xa3N\xdb\x87\xaf)%\xa3\xe3\xc4\x8b\x9c.\x81\xb5\x8c\x1b\xa8U@+\n\xed\xcb>;q\xd4\x1c\xb3\x88Y\x91Ew\xa9\xb0\xe2\x99-H\\+\xff\x99#\xf6\xb5\x13\xe3\xce\xce\x86\xbd\xed\x02\r\x19\xfbBS\xdd\xd6\x0e&\xde\x91\xcfw\xa4\\\xd9\xbb\xfalG?\xfa\xcd\xe6X\xb3\x7f\xd0\x9d9\x95d\xf9\xb7\x7f\x8f\xf0\xa2\xfb\x1af\x878\x8d(]\x0e\xa1`c\xf0v\xca\xfd\xdc\x8a\x80\x8e\xda+R\xcaPB\xd8\xf3\x1a\x13^6\xb5\xcc\xd1\xb8>\xcf6\x03\xfb\x02\xe0,1r\xc1\x92\xe6\xf8-(\xd5\xc7k\xe6a\xd1\x9fe\x13Hx\xd6\x9f\xbc\xbf\x9c\x8f\xa2\xf2U\xe5X\xbc\n\xd6wB\x9eu\x88#\xe6\xc2Ua\x13\xaaY[GJR\xbf\x1cf\xceyf\x05o3\xa0n+\xa3u\xe3\x95I[\x9f\xbaQ5\xf5\x1c\x9b\xdf\x02\xa4\xbd\xdc\x916{\x92\xad\xa5\x94\xa8\x95G8l\x98\x1c?\x91\xa4*Ws\x80M\xa4\xa5\nm\x1b\xf3\x12\x8c\x16Lf)W\x1d\xa7\xf8\x155\xe1\x99\xa4a\x1d\xae\x9a\xee\x94|\x93\x0f\xb5\xc4\xf0\x83\xdb\xee(Liy\xa8\x99\xd6\xad30(\xfb\xec@g\x16`\x95\xcaL4\xb1u_z\xadVQ^y\xac\xfb\x83T\x94\r4\xa0hc\x99A4\xfa\xa5\xa2\xddSr>\x01#\xc9\xf5S\x00q\xdf8\xdd\xe59\xe1\x91\xa0j\x17\'\x7fn\x86\xb7\xbda/\x01hD\x1b\xbf\xaf\xbb\x92+\x16\xe4\x9a\x12\xd9j\xcf\xe21J%\xc4H:VC\x83\xcf\xa1Q\xac\xa6;\xb2\xaa#\xcc\x0b_\x7fW\xf2\xec|\x9cn\xc5\xc8N\xcc\xae\n_8\x89\x9d&.\x10\x9e\x9f\x87\xa6\xaa\xb1O[J\x91?S\x14\t\xfa\x8f\x16=\xda\x87r\xac\x03\xe4\x1b\xdc\xed\xacW_\xdd\x19[\x02\x1f\xab\xd1L:\xa2\x10\x87\x90\x90\xe3\x89NJ\xb6\x8el=\x86 \xc0,\xab\xf3;J\x19\xa4\x0b!\x94\xe6I\x9b\x86/\xc3\xfc\xa3o\xe0\xbdOrJ\xe5\xffS\x8f\xc1\x86\x9e\x85BU\xd21!y\x8d\xb4\xdf\xd6#nv\x11K\xe6\x0b\x00\t&\x96\xbe\xaad\x97\x8e[u\xc6\xa8\xc5\xa6IL\xf9\xe9\x9cr\x04\xd8\xd3\xf4\x88p\xa8\xbf~\r\xe8\x93\xcaP^\xa6M\xbe\n\x0e\x1d5\x16\xb4\xce\xef\xb2J\xfdJ\xc2\x81\x9a:O\xa1*\x1b\xb1 \x90|NB\x90m\xc6\xb2\xcf\xa7\x02[\x16\xd8\x82\xbbd\'&\x8cyztRp,-\x93\xf3\x8e\x94E\xc7\xc5<\n\xc3\xba,\x82\x8c\xb8E\xce\xc5\xde\x8aX=\x87C\xa8\xca\xc2\'r\xbc\xc9w\x1bX\xdaOV\n\xd2Rb\xb8\x97}+\xd8a?\xae|\xa5?M\xff\xe2\x9d\\\xbe2\xb3\xf7\xd6\x07\xc3+2$x\xe8\xce&=4g\n=\xfb\xfd\xb8\xa3W\xd1\xb0]-k\x99\xc3\x82$\xb6\xbc\xda\xf4\xa6\x07\xf2\x1d\x9aQ;\x8b\x16\xc0(f\xd7A\xb7\xeb\xa8\xa3\x92\x97gw\x01\xb5\'\xdbm\x11\xf0\x87\x0b\xa1\xb2\x9aR5\nvf\x19\x10\xb6\xf7E\np\x9e\xbb{\xb8\x8bp;\xfdE`\x92\xe6\xd1\xa4\x86\xb6\'7\xd5yW31\xf0U\x15\x88$]\xbb\xd5\xaa\x1e\xc7O\x9f\xe2\xd6\x82\xaa0S\x94N\xc6\x12;\x9c\x89X\x96E$cPSZ}\xd6\x07\xd7\xd0\xc4gE\xc1\x92zM\xaa\xda\x96\xe9\xf1\xbf\xffe\xef\xf61\xcf\x16\xc5\xc84\x87W\x9dfU\xec_a\x88\xe1\xb3\xea\xd8l\x0b\xc9\xc1\xa4jBN\xc9\xbf\xc6\xc0\xda|\xc2\xca\xeb*y\xd8q\x7f\x00z\xa3$&x3\x98\xa7\x8eR\xf6\xe96\x98\x19\x9aQ\xee\xf3\x1b\xd4\xe16\rH(\xc3\xd7H\xbb\x1c_\xf8\x10\xe3\xdeT\xc3wG\xa0\x891\xa2<\n\xa6TBeC\x88oX#\xb2\x8bJrL\xff\xbagC)q\x8e2hM\x17\xa9,\xec\x9f\x92;\xc5!\xe9\x85\x94T+\xe0\xcd>\xf6K\xc4x\xafI%\xbb,u\x84\xcbFwF$\\>\x1b}\xb3l\xb9q\xc9\x1c8`\xed\n\xb3Y\x1c\x15\xbdq\xd8+]\x9e \x8d;(\xb1\x07\xb67\xdc\xbdn8\xbcRZ\x8f/\x97\x94NF\xc7\x8f9\xbb\x93\xbb\x98A\xef\x982\x95\x0bc\x19o\x0e\xf4E\x82\xbf\xbc\x9b\xb5\xb6\x88\x8dr\x06\xf72\xb4t\xba\x90\xf7\x8a\xd2\x10\xf0\xadO\x1c\x0b\xb2>\xc4\xac\xea.\\x\x8efH\xd1\xa5\xf6\xfa\x0e\xbb\x16\'\xefti\x89\x13\xa3\x99\xa41\xf0\x8c\x0by\x17\xb6\xa5qxI\x14N\xd3\x9e\x94\xfa|\xe7\xe5%\xf1\x9d\'\xab\x9d?B\xe9y<\x89\xccl\x8a\xd4,\x83\xe2ZG\xdc/\xa3\x1e\x04w+%\x16\xc4\xa8k\xd8\xc4p\x88)3\x8a\xc0\xb1r\xe8\x96g\x8b\xed\x0ckf\x8dz|\x00_w\xb4\xf7\x11h\xcf\xf9.\xc6\xac\xb0[\x87:C$_\xbf\xc3n3\x98\x1a\xe7\x93\r\x13\x02\xdd\xdbZ\xe7&E\xbe\xf91\xd6\x81P7\x9d^P\xa5\x0bU\xefn\xdb\xe5t;+\x93\xd9\xb1x`\xe30\xb7C\xee\xb9K\xc0,\xad/\xfd\x079\xca\xfaU\xc9\xdc\xf9\xd4\xf3M\x94_\x95\xfe\xef?\xff\xebm\xed\x8f.\xc4\xd1\xf6\xb2W\x16G0\xc6\xe2\x1d\x9e\xcbw\x81\xb3\x11\n\x00\xad7*\xe9B\r\x05#%\xf5\xbf\x04\xd8\xa1\xdew\xe5\x1d\xd6\xaf\xee\x9c\xbd\x18\xc1\x10\xbf\x813\xa4uS9k+z\xc8I\x87D\xc0?&\xa4G\x8f9\xc2C\xc4SX\xf3\xbdW-\x90X\x89*\xa8\xab\x9f\xc0\xb3\xc3\x913\xf3\xec\xf6\x0f\xd4]\x95\x9c\xe8~U\xd9\x05\xab@W\xea`K\x87r<0\x87j\xd9\xee\x14\\iQ\xd1B\x8b\x17\xc1\x1d\x83\xab8\xf5m\xed\xe8^t\xdfz\xceF\x81g\x17\xf7\x9f\x92\xff\xb9d\x14@yu\x1ft\x81\x96\xf2\xa1\xa3\x96[&\x1b\x97\xe8\xc5a.\x10eLOW\xc7\x98\xcd\xbat\xa73\xa0\xe3z\r\xabU\xccF\xf0\x8a\xb4:\xc6i\x88\x8bn\nL\xe3&\x0b\xd0p\xef\xebS\x89e\xd8\xa0\x8cc2\x1a\xfb\x96\xd2\x82\xf5v\xa2x\nF\xc1!\xd3\xcb^8e\xe2\x13\xf7\xd5m\xb7\x14\x03\xfd\\\xa2\xe7a\x9f\xf8\xcb\xf0c\xba\x10\x0f\xeaS\x99\xd9p\xd5j\xafq\x15\x1a^\x97\xf3\xf4\x9d\xb2\x1e\xd3\x84\xa3_ZP\x028\xe1\x8cW\x05j\x85o\x1c?\x9c\x8f\x91.t\xf7-\x8c\xdb\xce\x1f8$\xea~p\x90j\xee\xd7.e\x8aRs*Bcj\xca\xe5T\x85oH\xb3{\x9b%\xfd-P|\x1a~.?\xe4\x9f!\xc8\x06\x89\x1e\xe5\xe4=P\x02I\xddi\x1b\xbd{\x8a\xc7\x03\xe7\x83\xe5\x9d\xb0\x00\xb2\xeek\x12Z\xee\xc5S\xecu\xec}S\x8f\xd0cd\xd2F7\'4\x00\xc3I\xbeSN\x0co4\xc2a%\x84\xf93\xa1\x19\xcfZ1\xa7\x88H\x8a\xb9Uz\xf7u\x15\x0f\x05\xcd\x11{=gQ\x1e\x1f\x83\x1b!{F;\xcdy\xf2\xc0\xaa\xc7\xa2\x05\xb64_B\xa0\xa4fB\xd3{J\xa7\xf05\xe7\xd6\x16\x17\xe4`b\x8eQ\x95\xd5\x9cW79\xa9A\x90\x85\xd9\xcb\xfdY\xfe\xee\xc8\xdap\x99-\x82t%1b\xbb\xed\x03KO^3\x05\xff\xa0I7}M\x172)\x1c\xf5\x17Ji\xa4\x04\xab\\\xe3z\x14i8\x02G\xb5\x82Ou\xb6\xe7\x14>\x8dG\x8c3\xfb\xc2o\x98\x97\x98\x0c\x9d\xbb|\xc9\x08\x96m\xd5k\x1eR>\xd1V\xe62RDMb\xc5D\x97\xb9\xb0\x80\xbb\r\xa1L\x8bU\xe6\x80\xa8z\x01|4\xac\xc1l\xedN\x82\xd6J\xe4\xdb\x97p\xbf\xb2\xe3B)~\x85\x1b\xb8\xc4\xfbd\x82=f\x00\x8a\x81\xb1\x07[\xa6c\xd9\xb4\xbc;bU\x96t\x99!S\x0b\x00\xf23\'xdV\x81@_=}\xbd\xf2K\x0fYX\x9f\x01K\xb6\x19\xd42\xf7\xf8\xa5\xea<\xe7\xea\xe4ajV\n\x85N\xb1a7\x1b\xb9\xc9\x99\xeb\xff\xec\xa7O\xdem\xf2\xab5E\xd4\xca/\xa3\x93\xc9\x1f \xee\xb5+.\x97%\xac\x90\xafdf\xa1\x07,\x8ad=\xf0\x16\x14A\xa1;<\xdd&\xa6\xa1\xb0\xc8\xcb\x1a\xa6\xa9.\xc2\x14_\x80U\xd7\xf1\xd8r\xc8\x97b7\xe6U.+\xf8\xbe\x14\xed27\xc5b3\xa2\x89\xcc\xb1\xb24N%\xdf\xe9\xb7\t\xc2p\x92\xf5\x8dN2%\xefL3\x85\x15\x03i(]b\xf9tAc\x1c\xfa\x06\xaa\xae\xcd\xdb0\xde]O1\xf6\xce\x8d\x8e\x01\xa0\x07\xc9\x12\x99/\xfaO=\xde\xe1\xf2\x19\x1c-\x1d\xe1X\x18\x9e\x86\xc3\xd9\xb6\x9f$!J\xee\xa5\n\n\'\x1d=\xfb\x8d\x9cI\x15\xbd\xe1\xda\xab\x9d>\x16,\xa0=|(\x1dIe\xd6p\x143\xdc\x97\xd5`\xda\xfaW\x9d\xf1z\xf2\x15}\x9e\nz\xfa|\xe3V\x80\x9b\\\xec\xe6\x94G\xc3\xddrh\xaf\xda\xc5\x1c=2\x8c\x9c\x1e\xec8_\x8f\x16CR\x1a\xf9IwK\x12\x80@?+\xe2\x84\xba\xf6\xa7\xc0\xb8\x97)Q\xa0\xfc(\x96\xce\x9a0\x9a\x92\x06\xa5M\xba\x01\xd8\xab`\xf3\xc8\xa6\xd1\n\xc2\xd3<s\xd8p\x80\x98\xf9\x1ae\xc9\x1e\x1d\xad\x7f.\xd0\xde\xcb\x02\x99\x16h\xb8\x0b~\x0e\xf5\x96\xccR\x8f\x11\x9f\xc3\x0eyO\x9b\xeb:>\xae\xcc\xdcw\x98\t\x8bM\x99n-\xc2U\xa2\xb9\xe6J\xe5\x9d\xfa\x8c\xa9\x1e"\xc8t5U\xa3h\xf4\xcb0t\xb8\xe8Z\x86\xb8\x80\x00\x90\xbeQu\x0bnh\x15\xb8\xc8\xc5i\xbaq\x05W~n\x05\x9d!\xaaE.\x83\xc85l\x8aT\xb3\xe8\xab\x97\xf6|\xc6\xbe\xe0_\x80\xe1\'xHa\xa8\xa3H.\xd3\x16[\xa5\x9a9x\x915\x83\xd5*n\xf2+\xe7]Oi2\xe35\x96Cy#\xc3\x91\xdc\x81o\xe9+o\xec\xf4\xbe\xfc\xb0CL\x8b8\x99\xd0\x17\xfbF9\x1a4T\x1b\'\x07Y\x13I\x951\x8ag,\xff@\x8b\xf9_\xac\xa0\xb5\xc6+\xe7h\xf5?}=l`-zf+gTy\x1bQ\x165\xd2\xcd\x0f)\xbc#\xab\xb3qit\xc9L\xcb\xd4\x06e\xd2\xc0{\x89\x13->F\xa9^\x0c\xff4\n\x1b\xab]t\xe3\x94\x84+l\xf0\x1d9*\x9d\xaf\xf2\xd8jw\xe6\xdb\x1f\xc9\x1b\xfe\xfc\xee}*\xdc\x1b\xc3\xaf\xfa\x85\x8aZ)\x85\x8a\xce\xc8j\xc9\x9aW#r\xe1\x8fJ\xdd\xac\xf0\xc4yQ\xae\x85\n)\xf9R8zB)Dq\x89\xa6\xa3\x9cy\x01\x07\x99\xd4\xfb\xff\x9a0\xc4\x07Ci\\fa\xf8b\xaar\x8c8&q\x14\xcb\xdf\x93\x00\xde&\xcc\xac\x91\xa8v7 hH\x01Y$Wl\xd7\xcc\x19\x9fu\xb2!0+\xa5~^yV\x94q\xf2\xc5\xe9\xd9H\x93\x14\xfc\x0cl\xe5\x86\xc9\xe7\xf3F\xb3\xfd\xdf\x02\xc0\xf9\x87\xd3#\xd9i\xb9:Yhn(\x9b\xec\xd3y\xa0r\xd5\x1a\xd8\xf9\x1b\xc1\x8e2\x17\xac\x1c\x1dE\xe7u\xa7\x89\x98wQ\x9d1It\xd3\x03w\xcd\xf8\xd5\x18\xabqI\x81u\xf4\xdb?Jk2\xad\x91\xcf\xf4c_\x02\xe2\x95Cpk\xf0\x12F}g\xd2B\xd0F\xdfS,\x8e\x14\x85\x95\x93M^\xf6[\x0b\x81\xbb\x1f\x0e\xe8Y/\x1f\xab\xd12\xeaK\'\x98\xcfh\xfc\xe5\xac\xaeL\x87f=\x10\xf1\xc0\xbaPI\xa0\xa0\x96\x92\xec\x94\xd4\xe3\x18\x1d\xba2o8\xb6\xe6\xdd\xf0B\xb7\x8d\x99\xb0L\x14\xa1\x1e}s\x1e*>\x02\x9c\xc5M9\xb4\x1d\x052\xf8\x17W\xf2xtv\x95\xbeZ\xad\xa7\xae\x9e=\xf6i\x18\xa4L\x86\x12\xc35\xeb"\xa3?\xf76\xdcj\xce\x9f\xc4\xd8\'\x87\x19\x87\x8aty\xb7\x18F\xff\xff\xf7z#\x17k\x8d\x1c\x12h\xd8\xbf\xb3\x1e\xfa\xf5p\xf10\x7fMr\xab\xf0\x99\x9d\xdd\x08c\xa8Y\xb0cI\xfaq\x1a\xba\xdd\xf7)^yQ\x7f\x00x\xd6\x80uS\xa6\x18\rY\x9bQ\xa8\x83r\t6\xa1\xa9v\x17\xb7>3{t*=\xb0\xe9\'\x14\xa67\xee#\xb0\xb0f\xb6\xeem\r\x00\x14\xd5G\xf2\x94\xd9W\x9b\xedN\x7f\x0fN\x18\x90\x82\xe0`\xd5\xa7\xef\xde}\xe4\x1do~Y\xbf\xd9\xb8:\xceNR\xa6\xf9\x82C\xdaV\xd9$\xbb\x80\xa3&\x82p\xb5\xb9\xad\xb4\x85\xe3\x85M\xc1\x0e\x11\x9cw\xca\xf8\xcd\xd9\x94\x1a\xf0\xd3ZE\x10\xebO=<h7\xbe\xc7\xb18w\x10*\'?\xca5$#\xa2\x94V\x168\xa7S.]R\xa6I\xf6\xa5\xd9\xaf\xeb\xb2\x7f:r\xd5I\xd4\xbb\xd2\x80tn\x1d.\x13\x9b\xde\xdd\x0fn\xfa\x17\xbf\xc262\xca.\xab\xca{\xa4L\x9eEq\xb3\x01\xbeS\x01\xc8gw\xb2W\xe4\xad\xac\x91\x82\xdc\xa7\xceb\xa2\xd3\xfb\xdc\x93t}\x85\xfa\x1e\xb6\xd9\x90\x9e\xf3\xbe;\xaf\xddn\x08t\t\xfd\xd9\xe5\xe4\x18\xaf\x05|y\x89\x08\xc5V\xb5;\x8d\x7fze\x11\x8e\xc3q\x82\x10r\x0f]\x9e\x9f1&\xfaU(&F\xe0AX\x19\x06\\U\xf4\xb3:\xf4\xbb&\x12\xa5\xcc\xf4M\xdf4\x94\xa8s\r\xb0\xb6*\x11\xe1\x9c<\\Y\x03\xcez\x0e-%\x11\x8d3\xce\xa4|\xe0a\x98*\xe4\xe5eda=\x05\xfe\x11\x99\x01(\x1c#\x05\x15\x1c\x05\xeb\xf9\xa2\x00URm#\x04e\xca:\xbaHJ7\x9d\x8a\xa1\xdc\xa7\xd8\xae\xbc\xdb\x0fw\xcac\xdbZ\xbe5\x9f\xd4H\xfb\x07w\xca\x03\xd4\xdf\x19\xea\xebZY\x1f\x9e\xe3\xd5\xb9\xafg\xd7\x87\xd2W\xcc3\x97k\xfc\xcf\x7f~\xf9\x9f\xff\xa4_\xc5|\xf3\xf8\x12\x98\x0e\x7f\xe1\xdagR\x90#\xdd\xcf\xe3\xa0\x9f0\x87;\n.\xf5\x14\xf4\xb9\xf8\xa5\x85\x1c\xc8\xc8\xa8\xd1\x00\xd2\x02c\xda\xc5&\xf2\xafZ|\xea\x8e\xc5AA\xcc\xcb\x87\xd7\xf49r\xceGhV\x86\xa8\xb8\xef\xf2x\x90\x0f\x83\xf3\xe5\x0bZ\xcdfM\x81\xa9\xf1\xc1+|\xcd@w\x06>\x1d\xb9\\\'\x7f\xe2\x08\xfd\x00\x99\xed\xc61\x85\xcck=\xd1\xcd\xa11U1\x06\xfcE\x8892t\x1dW\xe4\xad\xee\xcb\x8btC\xa7\xd7\x94\xf7\xea~\xef\x83}\xc1\xce\xc9m]w\x94\x03\xf5\x9e\x7f\xd1d\xc2a\x1c#\xf4\xd7\x0c\x84\xe0\xdfP3\xe2.\xfe(l \x84al->\x19\x1e\xfa\xd9\x14\xf1\xf1\xbf\xf6M\xc5?\xecu\xe4_1\xc8\x9d\x90\xf37\x10\x1b\xd2\xd2\xa6\x85 N\xdd\xa01\xae\x01\x9b\x0e\xae4\xd5\x14\xc3e+@\x17\xe5G\xe9\x06\xa2\x9e8(\xc6\x9f\x8e\x0f\xdazK\xb9R\x13\xa2\xb6\xf3\rSB\x11\xe3\x03\xdd\x91\x18\xd5\x18r:\x0bU8d\xd1H\xd6-\xfd\xee,\xfd\xc0,\x85\x17\x1b|\x8b\x9d\xe1dr\x14\xb7\xc9\x89\xdaZ(\xd6\xc0|4eZ\x1e%6P\xc9\x95\xe0l\xa6\x0bW\x8aS\x15\xca<\x16\xb5\xabo\xe5[\xc6\xb5\x86_\xcb\x9d\xc7\xc6\x8f\x14\x81\xb5\xe2\x9f\xdf5\xebr\xdb\x1fw\x02\x18\x86T\xfb\xf9\x0e.UT>\xdf\xac\x1c~@\xd3\x14\xc0\r\xfa\xa0\xc4\xb2\xf2\xb7\xf9\xf2\xd4\xf1\xcf\x85\x0c"\x83-\xe2H\xbd\xb2[\x9a{0\xcbd\x12\xf8\x7f\xc5_\xd2J'
data = zlib.decompress(data).split("\n")

print random.choice(data)
