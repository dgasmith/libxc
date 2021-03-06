/* 
  This file was generated automatically with /nfs/data-012/marques/software/source/libxc/svn/scripts/maple2c.pl.
  Do not edit this file directly as it can be overwritten!!

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

  Maple version     : Maple 2016 (X86 64 LINUX)
  Maple source      : ../maple/gga_k_dk.mpl
  Type of functional: work_gga_x
*/

void xc_gga_k_dk_enhance
  (const xc_func_type *p,  xc_gga_work_x_t *r)
{
  double t1, t2, t3, t4, t6, t7, t9, t11;
  double t14, t15, t17, t19, t21, t24, t25, t26;
  double t27, t30, t37, t39, t40, t41, t50, t59;
  double t61, t65, t66, t67, t77, t95;

  gga_k_dk_params *params;
 
  assert(p->params != NULL);
  params = (gga_k_dk_params * )(p->params);

  t1 = params->aa[4];
  t2 = r->x * r->x;
  t3 = t2 * t2;
  t4 = t3 * t3;
  t6 = params->aa[3];
  t7 = t3 * t2;
  t9 = params->aa[2];
  t11 = params->aa[1];
  t14 = t1 * t4 + t11 * t2 + t9 * t3 + t6 * t7 + params->aa[0];
  t15 = params->bb[4];
  t17 = params->bb[3];
  t19 = params->bb[2];
  t21 = params->bb[1];
  t24 = t4 * t15 + t7 * t17 + t3 * t19 + t2 * t21 + params->bb[0];
  t25 = 0.1e1 / t24;
  r->f = t14 * t25;

  if(r->order < 1) return;

  t26 = t2 * r->x;
  t27 = t3 * t26;
  t30 = t3 * r->x;
  t37 = 0.2e1 * r->x * t11 + 0.8e1 * t27 * t1 + 0.4e1 * t26 * t9 + 0.6e1 * t30 * t6;
  t39 = t24 * t24;
  t40 = 0.1e1 / t39;
  t41 = t14 * t40;
  t50 = 0.2e1 * r->x * t21 + 0.8e1 * t27 * t15 + 0.6e1 * t30 * t17 + 0.4e1 * t26 * t19;
  r->dfdx = t37 * t25 - t41 * t50;

  if(r->order < 2) return;

  t59 = 0.56e2 * t7 * t1 + 0.12e2 * t2 * t9 + 0.30e2 * t3 * t6 + 0.2e1 * t11;
  t61 = t37 * t40;
  t65 = 0.1e1 / t39 / t24;
  t66 = t14 * t65;
  t67 = t50 * t50;
  t77 = 0.56e2 * t7 * t15 + 0.30e2 * t3 * t17 + 0.12e2 * t2 * t19 + 0.2e1 * t21;
  r->d2fdx2 = t59 * t25 - t41 * t77 - 0.2e1 * t61 * t50 + 0.2e1 * t66 * t67;

  if(r->order < 3) return;

  t95 = t39 * t39;
  r->d3fdx3 = (0.24e2 * r->x * t9 + 0.336e3 * t30 * t1 + 0.120e3 * t26 * t6) * t25 - 0.3e1 * t59 * t40 * t50 + 0.6e1 * t37 * t65 * t67 - 0.3e1 * t61 * t77 - 0.6e1 * t14 / t95 * t67 * t50 + 0.6e1 * t66 * t50 * t77 - t41 * (0.24e2 * r->x * t19 + 0.336e3 * t30 * t15 + 0.120e3 * t26 * t17);

  if(r->order < 4) return;


}

#define maple2c_order 3
#define maple2c_func  xc_gga_k_dk_enhance
