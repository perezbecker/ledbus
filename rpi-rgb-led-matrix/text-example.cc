// -*- mode: c++; c-basic-offset: 2; indent-tabs-mode: nil; -*-
// Small example how write text.
//
// This code is public domain
// (but note, that the led-matrix library this depends on is GPL v2)

#include "led-matrix.h"
#include "graphics.h"

#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

using namespace rgb_matrix;

static int usage(const char *progname) {
  fprintf(stderr, "usage: %s [options]\n", progname);
  fprintf(stderr, "Reads text from stdin and displays it. "
          "Empty string: clear screen\n");
  fprintf(stderr, "Options:\n"
          "\t-f <font-file>: Use given font.\n"
          "\t-r <rows>     : Display rows. 16 for 16x32, 32 for 32x32. "
          "Default: 32\n"
          "\t-P <parallel> : For Plus-models or RPi2: parallel chains. 1..3. "
          "Default: 1\n"
          "\t-c <chained>  : Daisy-chained boards. Default: 1.\n"
          "\t-x <x-origin> : X-Origin of displaying text (Default: 0)\n"
          "\t-y <y-origin> : Y-Origin of displaying text (Default: 0)\n"
          "\t-C <r,g,b>    : Color. Default 255,255,0\n");
  return 1;
}

static bool parseColor(Color *c, const char *str) {
  return sscanf(str, "%hhu,%hhu,%hhu", &c->r, &c->g, &c->b) == 3;
}

int main(int argc, char *argv[]) {
  Color color(255, 255, 0);
  const char *bdf_font_file = NULL;
  int rows = 32;
  int chain = 1;
  int parallel = 1;
  int x_orig = 0;
  int y_orig = -1;

  int opt;
  while ((opt = getopt(argc, argv, "r:P:c:x:y:f:C:")) != -1) {
    switch (opt) {
    case 'r': rows = atoi(optarg); break;
    case 'P': parallel = atoi(optarg); break;
    case 'c': chain = atoi(optarg); break;
    case 'x': x_orig = atoi(optarg); break;
    case 'y': y_orig = atoi(optarg); break;
    case 'f': bdf_font_file = strdup(optarg); break;
    case 'C':
      if (!parseColor(&color, optarg)) {
        fprintf(stderr, "Invalid color spec.\n");
        return usage(argv[0]);
      }
      break;
    default:
      return usage(argv[0]);
    }
  }

  if (bdf_font_file == NULL) {
    fprintf(stderr, "Need to specify BDF font-file with -f\n");
    return usage(argv[0]);
  }

  /*
   * Load font. This needs to be a filename with a bdf bitmap font.
   */
  rgb_matrix::Font font;
  if (!font.LoadFont(bdf_font_file)) {
    fprintf(stderr, "Couldn't load font '%s'\n", bdf_font_file);
    return usage(argv[0]);
  }

  if (rows != 16 && rows != 32) {
    fprintf(stderr, "Rows can either be 16 or 32\n");
    return 1;
  }

  if (chain < 1) {
    fprintf(stderr, "Chain outside usable range\n");
    return 1;
  }
  if (chain > 8) {
    fprintf(stderr, "That is a long chain. Expect some flicker.\n");
  }
  if (parallel < 1 || parallel > 3) {
    fprintf(stderr, "Parallel outside usable range.\n");
    return 1;
  }

  /*
   * Set up GPIO pins. This fails when not running as root.
   */
  GPIO io;
  if (!io.Init())
    return 1;

  /*
   * Set up the RGBMatrix. It implements a 'Canvas' interface.
   */
  RGBMatrix *canvas = new RGBMatrix(&io, rows, chain, parallel);

  bool all_extreme_colors = true;
  all_extreme_colors &= color.r == 0 || color.r == 255;
  all_extreme_colors &= color.g == 0 || color.g == 255;
  all_extreme_colors &= color.b == 0 || color.b == 255;
  if (all_extreme_colors)
    canvas->SetPWMBits(1);

  const int x = x_orig;
  int y = y_orig;

  if (isatty(STDIN_FILENO)) {
    // Only give a message if we are interactive. If connected via pipe, be quiet
    printf("Enter lines. Full screen or empty line clears screen.\n"
           "Supports UTF-8. CTRL-D for exit.\n");
  }

    char line[1024];
    while (fgets(line, sizeof(line), stdin)) {
   const size_t last = strlen(line);
    if (last > 0) line[last - 1] = '\0';  // remove newline.
    bool line_empty = strlen(line) == 0;
    if ((y + font.height() > canvas->height()) || line_empty) {
      canvas->Clear();
      y = y_orig;
    }
    if (line_empty)
      continue;

    char bus1[3];
    strncpy(bus1, line, 2);
    bus1[2] = (char)0;

    char bus2[3];
    strncpy(bus2, line+3, 2);
    bus2[2] = (char)0;

    char bus3[3];
    strncpy(bus3, line+6, 2);
    bus3[2] = (char)0;

    char bus4[3];
    strncpy(bus4, line+9, 2);
    bus4[2] = (char)0;

    char bus5[3];
    strncpy(bus5, line+12, 2);
    bus5[2] = (char)0;

    char bus6[3];
    strncpy(bus6, line+15, 2);
    bus6[2] = (char)0;

    char bus7[3];
    strncpy(bus7, line+18, 2);
    bus7[2] = (char)0;

    char bus8[3];
    strncpy(bus8, line+21, 2);
    bus8[2] = (char)0;

    char bus9[3];
    strncpy(bus9, line+24, 2);
    bus9[2] = (char)0;

    char bus10[3];
    strncpy(bus10, line+27, 2);
    bus10[2] = (char)0;

    char bus11[3];
    strncpy(bus11, line+30, 2);
    bus11[2] = (char)0;

    char bus12[3];
    strncpy(bus12, line+33, 2);
    bus12[2] = (char)0;



    //char time_since_last_response[3];
    //strncpy(time_since_last_response,line+18,2);
    //time_since_last_response[2] = (char)0;

    //int response_time_first_digit = time_since_last_response[0];
    //int response_time_second_digit = time_since_last_response[1];

    //int response_time = response_time_first_digit*10 + response_time_second_digit;

    int brightness = 130;

    Color white_(brightness,brightness,brightness);
    Color blue_(0,0,brightness);
    Color cyan_(0,brightness,brightness);
    Color green_(0,brightness,0);
    Color yellow_(brightness,brightness,0);
    Color red_(brightness,0,0);
    Color pink_(brightness,0,brightness);

    char white='w';
    char blue='b';
    char cyan='c';
    char green='g';
    char yellow='y';
    char red='r';
    char pink='p';

    int x1 = x;
    int x2 = x+11;
    int x3 = x+22;

    int x4 = x+33;
    int x5 = x+44;
    int x6 = x+55;

    int y1 = y + font.baseline();
    int y2 = y + 10 + font.baseline();


    char color1[2];
    strncpy(color1, line+2, 1);
    color1[1] = (char)0;
    if(color1[0] == white) rgb_matrix::DrawText(canvas, font, x1, y1, white_, bus1);
    if(color1[0] == blue) rgb_matrix::DrawText(canvas, font, x1, y1, blue_, bus1);
    if(color1[0] == cyan) rgb_matrix::DrawText(canvas, font, x1, y1, cyan_, bus1);
    if(color1[0] == green) rgb_matrix::DrawText(canvas, font, x1, y1, green_, bus1);
    if(color1[0] == yellow) rgb_matrix::DrawText(canvas, font, x1, y1, yellow_, bus1);
    if(color1[0] == red) rgb_matrix::DrawText(canvas, font, x1, y1, red_, bus1);
    if(color1[0] == pink) rgb_matrix::DrawText(canvas, font, x1, y1, pink_, bus1);

    char color2[2];
    strncpy(color2, line+5, 1);
    color2[1] = (char)0;
    if(color2[0] == white) rgb_matrix::DrawText(canvas, font, x2, y1, white_, bus2);
    if(color2[0] == blue) rgb_matrix::DrawText(canvas, font, x2, y1, blue_, bus2);
    if(color2[0] == cyan) rgb_matrix::DrawText(canvas, font, x2, y1, cyan_, bus2);
    if(color2[0] == green) rgb_matrix::DrawText(canvas, font, x2, y1, green_, bus2);
    if(color2[0] == yellow) rgb_matrix::DrawText(canvas, font, x2, y1, yellow_, bus2);
    if(color2[0] == red) rgb_matrix::DrawText(canvas, font, x2, y1, red_, bus2);
    if(color2[0] == pink) rgb_matrix::DrawText(canvas, font, x2, y1, pink_, bus2);

    char color3[2];
    strncpy(color3, line+8, 1);
    color3[1] = (char)0;
    if(color3[0] == white) rgb_matrix::DrawText(canvas, font, x3, y1, white_, bus3);
    if(color3[0] == blue) rgb_matrix::DrawText(canvas, font, x3, y1, blue_, bus3);
    if(color3[0] == cyan) rgb_matrix::DrawText(canvas, font, x3, y1, cyan_, bus3);
    if(color3[0] == green) rgb_matrix::DrawText(canvas, font, x3, y1, green_, bus3);
    if(color3[0] == yellow) rgb_matrix::DrawText(canvas, font, x3, y1, yellow_, bus3);
    if(color3[0] == red) rgb_matrix::DrawText(canvas, font, x3, y1, red_, bus3);
    if(color3[0] == pink) rgb_matrix::DrawText(canvas, font, x3, y1, pink_, bus3);

    char color4[2];
    strncpy(color4, line+11, 1);
    color4[1] = (char)0;
    if(color4[0] == white) rgb_matrix::DrawText(canvas, font, x1, y2, white_, bus4);
    if(color4[0] == blue) rgb_matrix::DrawText(canvas, font, x1, y2, blue_, bus4);
    if(color4[0] == cyan) rgb_matrix::DrawText(canvas, font, x1, y2, cyan_, bus4);
    if(color4[0] == green) rgb_matrix::DrawText(canvas, font, x1, y2, green_, bus4);
    if(color4[0] == yellow) rgb_matrix::DrawText(canvas, font, x1, y2, yellow_, bus4);
    if(color4[0] == red) rgb_matrix::DrawText(canvas, font, x1, y2, red_, bus4);
    if(color4[0] == pink) rgb_matrix::DrawText(canvas, font, x1, y2, pink_, bus4);

    char color5[2];
    strncpy(color5, line+14, 1);
    color5[1] = (char)0;
    if(color5[0] == white) rgb_matrix::DrawText(canvas, font, x2, y2, white_, bus5);
    if(color5[0] == blue) rgb_matrix::DrawText(canvas, font, x2, y2, blue_, bus5);
    if(color5[0] == cyan) rgb_matrix::DrawText(canvas, font, x2, y2, cyan_, bus5);
    if(color5[0] == green) rgb_matrix::DrawText(canvas, font, x2, y2, green_, bus5);
    if(color5[0] == yellow) rgb_matrix::DrawText(canvas, font, x2, y2, yellow_, bus5);
    if(color5[0] == red) rgb_matrix::DrawText(canvas, font, x2, y2, red_, bus5);
    if(color5[0] == pink) rgb_matrix::DrawText(canvas, font, x2, y2, pink_, bus5);

    char color6[2];
    strncpy(color6, line+17, 1);
    color6[1] = (char)0;
    if(color6[0] == white) rgb_matrix::DrawText(canvas, font, x3, y2, white_, bus6);
    if(color6[0] == blue) rgb_matrix::DrawText(canvas, font, x3, y2, blue_, bus6);
    if(color6[0] == cyan) rgb_matrix::DrawText(canvas, font, x3, y2, cyan_, bus6);
    if(color6[0] == green) rgb_matrix::DrawText(canvas, font, x3, y2, green_, bus6);
    if(color6[0] == yellow) rgb_matrix::DrawText(canvas, font, x3, y2, yellow_, bus6);
    if(color6[0] == red) rgb_matrix::DrawText(canvas, font, x3, y2, red_, bus6);
    if(color6[0] == pink) rgb_matrix::DrawText(canvas, font, x3, y2, pink_, bus6);

    char color7[2];
    strncpy(color7, line+20, 1);
    color7[1] = (char)0;
    if(color7[0] == white) rgb_matrix::DrawText(canvas, font, x4, y1, white_, bus7);
    if(color7[0] == blue) rgb_matrix::DrawText(canvas, font, x4, y1, blue_, bus7);
    if(color7[0] == cyan) rgb_matrix::DrawText(canvas, font, x4, y1, cyan_, bus7);
    if(color7[0] == green) rgb_matrix::DrawText(canvas, font, x4, y1, green_, bus7);
    if(color7[0] == yellow) rgb_matrix::DrawText(canvas, font, x4, y1, yellow_, bus7);
    if(color7[0] == red) rgb_matrix::DrawText(canvas, font, x4, y1, red_, bus7);
    if(color7[0] == pink) rgb_matrix::DrawText(canvas, font, x4, y1, pink_, bus7);

    char color8[2];
    strncpy(color8, line+23, 1);
    color8[1] = (char)0;
    if(color8[0] == white) rgb_matrix::DrawText(canvas, font, x5, y1, white_, bus8);
    if(color8[0] == blue) rgb_matrix::DrawText(canvas, font, x5, y1, blue_, bus8);
    if(color8[0] == cyan) rgb_matrix::DrawText(canvas, font, x5, y1, cyan_, bus8);
    if(color8[0] == green) rgb_matrix::DrawText(canvas, font, x5, y1, green_, bus8);
    if(color8[0] == yellow) rgb_matrix::DrawText(canvas, font, x5, y1, yellow_, bus8);
    if(color8[0] == red) rgb_matrix::DrawText(canvas, font, x5, y1, red_, bus8);
    if(color8[0] == pink) rgb_matrix::DrawText(canvas, font, x5, y1, pink_, bus8);

    char color9[2];
    strncpy(color9, line+26, 1);
    color9[1] = (char)0;
    if(color9[0] == white) rgb_matrix::DrawText(canvas, font, x6, y1, white_, bus9);
    if(color9[0] == blue) rgb_matrix::DrawText(canvas, font, x6, y1, blue_, bus9);
    if(color9[0] == cyan) rgb_matrix::DrawText(canvas, font, x6, y1, cyan_, bus9);
    if(color9[0] == green) rgb_matrix::DrawText(canvas, font, x6, y1, green_, bus9);
    if(color9[0] == yellow) rgb_matrix::DrawText(canvas, font, x6, y1, yellow_, bus9);
    if(color9[0] == red) rgb_matrix::DrawText(canvas, font, x6, y1, red_, bus9);
    if(color9[0] == pink) rgb_matrix::DrawText(canvas, font, x6, y1, pink_, bus9);

    char color10[2];
    strncpy(color10, line+29, 1);
    color10[1] = (char)0;
    if(color10[0] == white) rgb_matrix::DrawText(canvas, font, x4, y2, white_, bus10);
    if(color10[0] == blue) rgb_matrix::DrawText(canvas, font, x4, y2, blue_, bus10);
    if(color10[0] == cyan) rgb_matrix::DrawText(canvas, font, x4, y2, cyan_, bus10);
    if(color10[0] == green) rgb_matrix::DrawText(canvas, font, x4, y2, green_, bus10);
    if(color10[0] == yellow) rgb_matrix::DrawText(canvas, font, x4, y2, yellow_, bus10);
    if(color10[0] == red) rgb_matrix::DrawText(canvas, font, x4, y2, red_, bus10);
    if(color10[0] == pink) rgb_matrix::DrawText(canvas, font, x4, y2, pink_, bus10);

    char color11[2];
    strncpy(color11, line+32, 1);
    color11[1] = (char)0;
    if(color11[0] == white) rgb_matrix::DrawText(canvas, font, x5, y2, white_, bus11);
    if(color11[0] == blue) rgb_matrix::DrawText(canvas, font, x5, y2, blue_, bus11);
    if(color11[0] == cyan) rgb_matrix::DrawText(canvas, font, x5, y2, cyan_, bus11);
    if(color11[0] == green) rgb_matrix::DrawText(canvas, font, x5, y2, green_, bus11);
    if(color11[0] == yellow) rgb_matrix::DrawText(canvas, font, x5, y2, yellow_, bus11);
    if(color11[0] == red) rgb_matrix::DrawText(canvas, font, x5, y2, red_, bus11);
    if(color11[0] == pink) rgb_matrix::DrawText(canvas, font, x5, y2, pink_, bus11);

    char color12[2];
    strncpy(color12, line+35, 1);
    color12[1] = (char)0;
    if(color12[0] == white) rgb_matrix::DrawText(canvas, font, x6, y2, white_, bus12);
    if(color12[0] == blue) rgb_matrix::DrawText(canvas, font, x6, y2, blue_, bus12);
    if(color12[0] == cyan) rgb_matrix::DrawText(canvas, font, x6, y2, cyan_, bus12);
    if(color12[0] == green) rgb_matrix::DrawText(canvas, font, x6, y2, green_, bus12);
    if(color12[0] == yellow) rgb_matrix::DrawText(canvas, font, x6, y2, yellow_, bus12);
    if(color12[0] == red) rgb_matrix::DrawText(canvas, font, x6, y2, red_, bus12);
    if(color12[0] == pink) rgb_matrix::DrawText(canvas, font, x6, y2, pink_, bus12);


    //rgb_matrix::DrawText(canvas, font, x+11, y + font.baseline(), blue_, secondbus);
    //rgb_matrix::DrawText(canvas, font, x+22, y + font.baseline(), cyan_, thirdbus);
    //rgb_matrix::DrawText(canvas, font, x, y + font.baseline()+10, green_, bus4);
    //rgb_matrix::DrawText(canvas, font, x+11, y + font.baseline()+10, yellow_, bus5);
    //rgb_matrix::DrawText(canvas, font, x+22, y + font.baseline()+10, red_, bus6);

    //rgb_matrix::DrawText(canvas, font, x1 -10 +response_time , y + 15 + font.baseline(), cyan_, "|");

    y += font.height()+ font.height();
  }


  // Finished. Shut down the RGB matrix.
  canvas->Clear();
  delete canvas;

  return 0;
}
