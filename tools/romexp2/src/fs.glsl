#version 130

out vec4 out_color;
uniform uint ww;
uniform uint wh;
uniform uint stride;

uniform usampler1D romtex;

void main() {
     uint x = uint(gl_FragCoord[0] - 0.5);
     uint y = (wh - 1u) - uint(gl_FragCoord[1] - 0.5);
     uint col = x / stride;
     uint bitidx = ((y  + (col*wh)) * stride) + (x % stride);
     
     uint tex_off = bitidx / 8u;
     uint tex_bit_off = bitidx % 8u;

     if (tex_off >= {}u) {
     	out_color = vec4(0.0,0.0,0.4,1.0);
     	return;
	}	
     uint rv = (texture(romtex, (float(tex_off)+0.5)/{}.0).r >> (7u-tex_bit_off)) & 1u;
     out_color = vec4(float(rv),float(rv),float(rv), 1.0);
}
