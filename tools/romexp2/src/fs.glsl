#version 130

out vec4 out_color;
uniform uint ww;
uniform uint wh;
uniform uint stride;
uniform uint rom[{}];

void bitfieldExtract(in uint word, in uint offset, out uint rv) {
     uint newoff = (3u-(offset / 8u))*8u + (offset%8u);
     rv = (word >> newoff) & 1u;
}
     
void main() {
     uint x = uint(gl_FragCoord[0] - 0.5);
     uint y = (wh - 1u) - uint(gl_FragCoord[1] - 0.5);
     uint rlen = uint({});
     uint col = x / stride;
     uint bitidx = ((y  + (col*wh)) * stride) + (x % stride);
     
     uint word_off = (bitidx / 32u) % uint({});
     uint bit_off = bitidx % 32u;
     uint rv = 0u;
     bitfieldExtract(rom[word_off],31u-bit_off,rv);
     out_color = vec4(float(rv)/1.0,float(rv)/1.0,float(rv)/1.0, 1.0);
}
