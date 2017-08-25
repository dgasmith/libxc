/*
 Copyright (C) 2015 M.A.L. Marques, Markus Patzold

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.
  
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.
  
 You should have received a copy of the GNU Lesser General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#include "util.h"

#define XC_GGA_X_GG99   535 /* Gilbert and Gill 1999 */
#define XC_GGA_X_KGG99  544 /* Gilbert and Gill 1999 (mixed) */

static void
newt_raph(double a, double tol, double *xx, double *dxx, int *ierr)
{
  int count;
  double x, f, fp;
  static int max_iter = 50;

  *ierr = 1;
   
  /* starting point */
  x = 1.0;

  count = 0;
  do {
    double sh, ch;
     
    sh = sinh(x);
    ch = cosh(x);
    
    f  = 2.0*M_PI*sh/CBRT(3.0*ch) - a;
    fp = 2.0*M_PI*(2.0 + ch*ch + sh*sh)/(3.0*M_CBRT3*ch*CBRT(ch));
    
    x -= f/fp;
    
    count ++;
  } while((fabs(f) > tol) && (count < max_iter));
  
  if(count == max_iter) *ierr=0; 

  *xx  = x;
  *dxx = 1.0/fp;
}


/* This implements Eq. (22) of the paper */
inline static void 
r_x(int order, double x, double *r, double *dr)
{
  static const double
    a1 = 4.0*M_SQRT3*M_PI*M_PI*M_PI;

  double a2, x2, x4, x6, aux1, aux2, daux1, daux2, num, den, dd, dnum, dden;
  int ierr;

  a2 = SQRT(3.0/(2.0*a1));

  x2 = x*x;
  x4 = x2*x2;
  x6 = x2*x4;

  if(a1*a1 > x6){
    aux1 = a1 + SQRT(a1*a1 - x6);
    aux2 = CBRT(aux1);

    num = x*a2*SQRT(x2 + aux2*aux2);
    den = SQRT(aux2);
  
    *r = asinh(num/den);
  }else{ // asymptotic expansion
    newt_raph(x, 1e-12, r, dr, &ierr);
  }

  if(order < 1) return;

  if(a1*a1 > x6){
    daux1 = -3.0*x*x4/SQRT(a1*a1 - x6);
    daux2 = daux1*aux2/(3.0*aux1);

    dnum = a2*(2.0*x2 + aux2*aux2 + x*aux2*daux2)/SQRT(x2 + aux2*aux2);
    dden = daux2*den/(2.0*aux2);

    dd  = DFRACTION(num, dnum, den, dden);
    *dr = dd/SQRT(1 + num*num/(den*den));
  }
}

void XC(gga_x_gg99_enhance)
     (const XC(func_type) *p, XC(gga_work_x_t) *r)
{
  double rr, dr;
  double aux1, aux2, aux3, aux4, aux5, daux1, daux2, daux4, daux5;
  double num, den, dnum, dden, df;

  r_x(r->order, r->x, &rr, &dr);

  aux1 = exp(-2.0*rr);

  aux2 = log(1.0 + aux1);
  aux3 = 1.0/cosh(rr);
  aux4 = pow(aux3, 2.0/3.0);
  aux5 = XC(dilogarithm)(-aux1);

  num = -M_PI*M_PI + 12.0*rr*aux2 - 12.0*aux5;
  den = 2.0*M_CBRT3*M_PI*rr*aux4;

  r->f = num/(X_FACTOR_C*den);
    
  if(r->order < 1) return;

  daux1 = -2.0*aux1;
  daux2 = daux1/(1.0 + aux1);
  daux4 = -2.0/3.0*aux4*tanh(rr);
  daux5 = -aux2*daux1/aux1;

  dnum = 12.0*(aux2 + rr*daux2) - 12.0*daux5;
  dden = 2.0*M_CBRT3*M_PI*(aux4 + rr*daux4);

  r->dfdx = DFRACTION(num, dnum, den, dden)*dr/X_FACTOR_C;
}

#define func XC(gga_x_gg99_enhance)
#include "work_gga_x.c"

const XC(func_info_type) XC(func_info_gga_x_gg99) = {
  XC_GGA_X_GG99,
  XC_EXCHANGE,
  "Gilbert and Gill 1999",
  XC_FAMILY_GGA,
  {&xc_ref_Gilbert1999_511, NULL, NULL, NULL, NULL},
  XC_FLAGS_3D | XC_FLAGS_HAVE_EXC | XC_FLAGS_HAVE_VXC,
  1e-32,
  0, NULL, NULL,
  NULL, NULL, 
  NULL, work_gga_x, NULL
};


/*************************************************************/
static void
gga_c_kgg_init(XC(func_type) *p)
{
  /* defined in Eq. (25) of the paper */
  static int   funcs_id  [2] = {XC_LDA_X, XC_GGA_X_GG99};
  static double funcs_coef[2] = {-0.047/X_FACTOR_C, 1.0};

  XC(mix_init)(p, 2, funcs_id, funcs_coef);
}

const XC(func_info_type) XC(func_info_gga_x_kgg99) = {
  XC_GGA_X_KGG99,
  XC_EXCHANGE,
  "Gilbert and Gill 1999 (mixed)",
  XC_FAMILY_GGA,
  {&xc_ref_Gilbert1999_511, NULL, NULL, NULL, NULL},
  XC_FLAGS_3D | XC_FLAGS_HAVE_EXC | XC_FLAGS_HAVE_VXC,
  1e-32,
  0, NULL, NULL,
  gga_c_kgg_init, NULL, 
  NULL, NULL, NULL
};

