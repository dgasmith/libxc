(*
 Copyright (C) 2017 M.A.L. Marques

 This Source Code Form is subject to the terms of the Mozilla Public
 License, v. 2.0. If a copy of the MPL was not distributed with this
 file, You can obtain one at http://mozilla.org/MPL/2.0/.
*)

(* type: work_mgga_x *)

e1 := -1.6665:
c1 :=  0.7438:

fa := a -> (1 - a) / ((1 + e1*a^2)^2 + c1*a^4):

k0 := 0.174:
b  := 0.0233:

f := (rs, x, t, u) -> (1 + k0*fa((t - x^2/8)/K_FACTOR_C)) /   \
  (1 + b*X2S^4*x^4)^(1/8):
