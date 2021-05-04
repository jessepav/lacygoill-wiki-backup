# Document these functions:

   - `:h sign_define()`
   - `:h sign_getdefined()`
   - `:h sign_getplaced()`
   - `:h sign_jump()`
   - `:h sign_place()`
   - `:h sign_placelist()`
   - `:h sign_undefine()`
   - `:h sign_unplace()`
   - `:h sign_unplacelist()`

# Document one advantage of signs over matches.

They can highlight a whole screen line  (with the `linehl` key), whereas a match
ends on the last buffer character on the line.

# Implement motions jumping to next/previous/first/last sign.

# Automatically set signs after the qfl is populated.

Remove stale signs when a new qfl is added onto the stack, or visited (via `:colder`, `:cnewer`).
Create mapping to clear qfl (`=q`) so that signs are cleared.

# Study signs in popups.

It seems you can't get them via `sign_getplaced()`.
Actually, you get  sth weird; you have  the buffer numbers where  signs are set,
but not the signs themselves (empty list).  Even weirder, once you undefine the
signs, you get the same output (I would expect an empty list; no buffer numbers).

You can remove them via `sign_unplace()`.
But if you do,  and the popup had a sign column, the  latter disappears, even if
`'scl'` is 'yes'.  Bug?

What does this sentence from `:h sign-group` mean:

   > The group name "PopUpMenu" is used by popup windows where 'cursorline' is set.

Does it mean we must use this prefix when 'cursorline' is set?
Or does it mean we must use this prefix for a popup menu created with `popup_menu()`?
What happens if we don't use this prefix?

---

For the moment, the best way I've found to remove signs in popups is `sign_undefine()`.
But it requires `sil!`.
Is there sth better?
If you find sth better, fix `SetSign()` in:

    ~/.vim/pack/mine/opt/qf/autoload/qf/preview.vim

I don't think we can test the existence of the signs.
It would be possible if `sign_getplaced()` returned an empty list once the signs
are undefined, but that's not the case...

Anyway,  once   you  better   understand  the  situation,   consider  commenting
`sign_undefine()` in `SetSign()` in `preview.vim`.

---

Which sign functions work with popup windows?
Which sign functions do *not* work with popup windows?

Actually, do these questions make sense?
I mean, signs are local to buffers, not windows...

---

What happens  when we set  a sign  **with** the group  prefix name `PopUp`  in a
buffer displayed in both a regular window and a popup window?

What happens when we  set a sign **without** the group prefix  name `PopUp` in a
buffer displayed in both a regular window and a popup window?

# What's the effect of `sign_undefine()` in a regular buffer with signs?

# Are signs local to a buffer?

If I set a sign in a buffer, does it persist no matter the window in which I display it?

