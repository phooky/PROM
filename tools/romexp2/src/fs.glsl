#version 130

out vec4 out_color;
uniform uint ww;
uniform uint wh;
uniform uint rom[{}];
void main() {
     uint bitidx = uint(gl_FragCoord[0]) + uint(gl_FragCoord[1]) * ww;
     uint word_off = (bitidx / 32u) % uint({});
     uint bit_off = bitidx % 32u;
     uint rv = (rom[word_off] >> (31u-bit_off)) & 1u;
     out_color = vec4(float(rv)/1.0,float(rv)/1.0,float(rv)/1.0, 1.0);
}
