/* 
  This file was generated automatically with /nfs/data-012/marques/software/source/libxc/svn/scripts/maple2c.pl.
  Do not edit this file directly as it can be overwritten!!

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Maple version     : Maple 2016 (X86 64 LINUX)
  Maple source      : ../maple/mgga_x_mvs.mpl
  Type of functional: work_mgga_x
*/

static void 
xc_mgga_x_mvs_enhance(const xc_func_type *pt, xc_mgga_work_x_t *r)
{
  double t1, t3, t4, t6, t7, t8, t9, t12;
  double t13, t14, t17, t20, t21, t22, t24, t26;
  double t29, t30, t33, t34, t35, t38, t39, t40;
  double t41, t45, t46, t47, t48, t53, t54, t57;
  double t60, t63, t64, t66, t69, t70, t72, t74;
  double t76, t79, t81, t87, t88, t91, t108, t123;
  double t128;


  t1 = r->x * r->x;
  t3 = r->t - t1 / 0.8e1;
  t4 = M_CBRT6;
  t6 = 0.31415926535897932385e1 * 0.31415926535897932385e1;
  t7 = POW_1_3(t6);
  t8 = t7 * t7;
  t9 = 0.1e1 / t8;
  t12 = 0.1e1 - 0.5e1 / 0.9e1 * t3 * t4 * t9;
  t13 = t3 * t3;
  t14 = t4 * t4;
  t17 = 0.1e1 / t7 / t6;
  t20 = 0.1e1 - 0.51435185185185185185e0 * t13 * t14 * t17;
  t21 = t20 * t20;
  t22 = t13 * t13;
  t24 = t6 * t6;
  t26 = 0.1e1 / t8 / t24;
  t29 = t21 + 0.42512574302697759488e0 * t22 * t4 * t26;
  t30 = 0.1e1 / t29;
  t33 = 0.1e1 + 0.174e0 * t12 * t30;
  t34 = t14 * t17;
  t35 = t1 * t1;
  t38 = 0.1e1 + 0.40451388888888888890e-4 * t34 * t35;
  t39 = pow(t38, 0.1e1 / 0.8e1);
  t40 = 0.1e1 / t39;
  r->f = t33 * t40;

  if(r->order < 1) return;

  r->dfdrs = 0.0e0;
  t41 = r->x * t4;
  t45 = t29 * t29;
  t46 = 0.1e1 / t45;
  t47 = t12 * t46;
  t48 = t20 * t3;
  t53 = t13 * t3 * t4;
  t54 = t26 * r->x;
  t57 = 0.51435185185185185184e0 * t48 * t34 * r->x - 0.42512574302697759488e0 * t53 * t54;
  t60 = 0.24166666666666666667e-1 * t41 * t9 * t30 - 0.174e0 * t47 * t57;
  t63 = 0.1e1 / t39 / t38;
  t64 = t33 * t63;
  t66 = t34 * t1 * r->x;
  r->dfdx = t60 * t40 - 0.20225694444444444445e-4 * t64 * t66;
  t69 = t4 * t9;
  t70 = t69 * t30;
  t72 = t48 * t34;
  t74 = t53 * t26;
  t76 = -0.20574074074074074074e1 * t72 + 0.17005029721079103795e1 * t74;
  t79 = -0.96666666666666666667e-1 * t70 - 0.174e0 * t47 * t76;
  r->dfdt = t79 * t40;
  r->dfdu = 0.0e0;

  if(r->order < 2) return;

  r->d2fdrs2 = 0.0e0;
  t81 = t9 * t46;
  t87 = t12 / t45 / t29;
  t88 = t57 * t57;
  t91 = t13 * t4;
  t108 = t38 * t38;
  r->d2fdx2 = (0.24166666666666666667e-1 * t70 - 0.48333333333333333334e-1 * t41 * t81 * t57 + 0.348e0 * t87 * t88 - 0.174e0 * t47 * (0.11125177897805212620e1 * t91 * t26 * t1 - 0.12858796296296296296e0 * t20 * t1 * t34 + 0.51435185185185185184e0 * t72 - 0.42512574302697759488e0 * t74)) * t40 - 0.40451388888888888890e-4 * t60 * t63 * t66 + 0.22090250651041666667e-7 * t33 / t39 / t108 * t4 * t26 * t35 * t1 - 0.60677083333333333335e-4 * t64 * t34 * t1;
  t123 = t76 * t76;
  t128 = t20 * t14;
  r->d2fdt2 = (0.19333333333333333333e0 * t69 * t46 * t76 + 0.348e0 * t87 * t123 - 0.174e0 * t47 * (0.17800284636488340192e2 * t91 * t26 - 0.20574074074074074074e1 * t128 * t17)) * t40;
  r->d2fdu2 = 0.0e0;
  r->d2fdrsx = 0.0e0;
  r->d2fdrst = 0.0e0;
  r->d2fdrsu = 0.0e0;
  r->d2fdxt = (-0.24166666666666666667e-1 * t41 * t81 * t76 + 0.96666666666666666667e-1 * t69 * t46 * t57 + 0.348e0 * t87 * t57 * t76 - 0.174e0 * t47 * (-0.44500711591220850479e1 * t91 * t54 + 0.51435185185185185184e0 * t128 * t17 * r->x)) * t40 - 0.20225694444444444445e-4 * t79 * t63 * t66;
  r->d2fdxu = 0.0e0;
  r->d2fdtu = 0.0e0;

  if(r->order < 3) return;


}

#define maple2c_order 3
#define maple2c_func  xc_mgga_x_mvs_enhance
