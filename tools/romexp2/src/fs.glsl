#version 130

out vec4 out_color;
uniform uint ww;
uniform uint wh;
uniform uint stride;
uniform uint romh;

uniform usampler2D romtex;

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
    uint tex_off_x = tex_off % 16384u;
    uint tex_off_y = tex_off / 16384u;
    vec2 coord = vec2( (float(tex_off_x)+0.5) / 16384.0, (float(tex_off_y)+0.5) / float(romh) );
     uint rv = (texture(romtex, coord).r >> (7u-tex_bit_off)) & 1u;
     out_color = vec4(float(rv),float(rv),float(rv), 1.0);
}
