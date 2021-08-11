let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Códigos/Mill_Back-calculation_Notebook
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 index.py
badd +1 app.py
badd +1 app/widgets.py
badd +36 app/__init__.py
badd +1 app/simulation.py
badd +107 app/figures.py
badd +1 app/input.py
badd +109 app/layout.py
badd +30 app/retrocalc.py
argglobal
%argdel
$argadd app.py
edit app/input.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
wincmd _ | wincmd |
vsplit
2wincmd h
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 75 + 113) / 227)
exe 'vert 2resize ' . ((&columns * 75 + 113) / 227)
exe 'vert 3resize ' . ((&columns * 75 + 113) / 227)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 3 - ((2 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3
normal! 0
wincmd w
argglobal
if bufexists("index.py") | buffer index.py | else | edit index.py | endif
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
if bufexists("app/__init__.py") | buffer app/__init__.py | else | edit app/__init__.py | endif
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
50
normal! zo
51
normal! zo
51
normal! zo
55
normal! zo
56
normal! zo
56
normal! zo
61
normal! zo
61
normal! zo
61
normal! zc
let s:l = 36 - ((35 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
36
normal! 0
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 75 + 113) / 227)
exe 'vert 2resize ' . ((&columns * 75 + 113) / 227)
exe 'vert 3resize ' . ((&columns * 75 + 113) / 227)
tabedit app/widgets.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
wincmd _ | wincmd |
vsplit
2wincmd h
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 75 + 113) / 227)
exe 'vert 2resize ' . ((&columns * 75 + 113) / 227)
exe 'vert 3resize ' . ((&columns * 75 + 113) / 227)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
118
normal! zo
118
normal! zo
let s:l = 3 - ((2 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3
normal! 03|
wincmd w
argglobal
if bufexists("app/layout.py") | buffer app/layout.py | else | edit app/layout.py | endif
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
66
normal! zo
66
normal! zo
let s:l = 73 - ((72 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
73
normal! 0
wincmd w
argglobal
if bufexists("app/figures.py") | buffer app/figures.py | else | edit app/figures.py | endif
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
44
normal! zo
54
normal! zo
67
normal! zo
72
normal! zo
79
normal! zo
79
normal! zo
87
normal! zo
let s:l = 54 - ((53 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
54
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 75 + 113) / 227)
exe 'vert 2resize ' . ((&columns * 75 + 113) / 227)
exe 'vert 3resize ' . ((&columns * 75 + 113) / 227)
tabedit app/simulation.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 113 + 113) / 227)
exe 'vert 2resize ' . ((&columns * 113 + 113) / 227)
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
114
normal! zo
let s:l = 130 - ((125 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
130
normal! 0
wincmd w
argglobal
if bufexists("app/retrocalc.py") | buffer app/retrocalc.py | else | edit app/retrocalc.py | endif
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=99
setlocal fml=1
setlocal fdn=20
setlocal fen
10
normal! zo
10
normal! zo
44
normal! zo
48
normal! zo
48
normal! zc
59
normal! zo
60
normal! zo
66
normal! zo
let s:l = 38 - ((37 * winheight(0) + 27) / 55)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
38
normal! 06|
wincmd w
exe 'vert 1resize ' . ((&columns * 113 + 113) / 227)
exe 'vert 2resize ' . ((&columns * 113 + 113) / 227)
tabnext 1
if exists('s:wipebuf') && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 winminheight=1 winminwidth=1 shortmess=filnxtToOF
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
