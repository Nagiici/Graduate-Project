/* -----------------------------------------------
/* Author : Vincent Garreau - vincentgarreau.com
/* MIT license: http://opensource.org/licenses/MIT
/* Demo / Generator : https://vincentgarreau.com/particles.js
/* GitHub : https://github.com/VincentGarreau/particles.js
/* How to use? : Check the GitHub README
/* v2.0.0
/* ----------------------------------------------- */

var particlesJS = function(tag_id, params){

    /* params setting */
    if(!params)
      params = {};
  
    /* canvas setup */
    var canvas_el = document.createElement('canvas');
    var ctx = canvas_el.getContext('2d');
  
    canvas_el.style.position = 'fixed';
    canvas_el.style.top = 0;
    canvas_el.style.left = 0;
    canvas_el.style.width = '100%';
    canvas_el.style.height = '100%';
    canvas_el.style.zIndex = -1;
    canvas_el.style.pointerEvents = 'none';
  
    document.getElementById(tag_id).appendChild(canvas_el);
  
    /* default settings */
    var pJS = {
      canvas: {
        el: canvas_el,
        w: canvas_el.offsetWidth,
        h: canvas_el.offsetHeight,
        ctx: ctx
      },
      particles: {
        number: {
          value: 100,
          density: {
            enable: true,
            value_area: 800
          }
        },
        color: {
          value: '#ffffff'
        },
        shape: {
          type: 'circle',
          stroke: {
            width: 0,
            color: '#000000'
          },
          polygon: {
            nb_sides: 5
          }
        },
        opacity: {
          value: 0.5,
          random: false,
          anim: {
            enable: false,
            speed: 1,
            opacity_min: 0.1,
            sync: false
          }
        },
        size: {
          value: 3,
          random: true,
          anim: {
            enable: false,
            speed: 40,
            size_min: 0.1,
            sync: false
          }
        },
        line_linked: {
          enable: true,
          distance: 150,
          color: '#ffffff',
          opacity: 0.4,
          width: 1
        },
        move: {
          enable: true,
          speed: 6,
          direction: 'none',
          random: false,
          straight: false,
          out_mode: 'out',
          bounce: false,
          attract: {
            enable: false,
            rotateX: 600,
            rotateY: 1200
          }
        }
      },
      interactivity: {
        detect_on: 'canvas',
        events: {
          onhover: {
            enable: true,
            mode: 'grab'
          },
          onclick: {
            enable: true,
            mode: 'push'
          },
          resize: true
        },
        modes: {
          grab: {
            distance: 140,
            line_linked: {
              opacity: 1
            }
          },
          bubble: {
            distance: 400,
            size: 40,
            duration: 2,
            opacity: 8,
            speed: 3
          },
          repulse: {
            distance: 200,
            duration: 0.4
          },
          push: {
            particles_nb: 4
          },
          remove: {
            particles_nb: 2
          }
        }
      },
      retina_detect: true
    };
  
    /* merge params */
    for(var key in params){
      if(params.hasOwnProperty(key)){
        pJS[key] = params[key];
      }
    }
  
    /* particles creation */
    var pJSDom = pJS;
    var particles = [];
  
    pJSDom.fn = {
      particlesCreate: function(){
        for(var i = 0; i < pJSDom.particles.number.value; i++){
          particles.push(new pJSDom.fn.particle());
        }
      },
      particle: function(){
        this.x = Math.random() * pJSDom.canvas.w;
        this.y = Math.random() * pJSDom.canvas.h;
        this.vx = (Math.random() - 0.5) * pJSDom.particles.move.speed;
        this.vy = (Math.random() - 0.5) * pJSDom.particles.move.speed;
        this.color = pJSDom.particles.color.value;
        this.size = pJSDom.particles.size.value;
        this.opacity = pJSDom.particles.opacity.value;
        this.draw = function(){
          pJSDom.canvas.ctx.fillStyle = this.color;
          pJSDom.canvas.ctx.globalAlpha = this.opacity;
          pJSDom.canvas.ctx.beginPath();
          pJSDom.canvas.ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
          pJSDom.canvas.ctx.fill();
        };
        this.update = function(){
          this.x += this.vx;
          this.y += this.vy;
  
          if(this.x - this.size > pJSDom.canvas.w){
            this.x = -this.size;
          } else if(this.x + this.size < 0){
            this.x = pJSDom.canvas.w + this.size;
          }
  
          if(this.y - this.size > pJSDom.canvas.h){
            this.y = -this.size;
          } else if(this.y + this.size < 0){
            this.y = pJSDom.canvas.h + this.size;
          }
  
          this.draw();
        };
      }
    };
  
    /* animation loop */
    function animate(){
      requestAnimationFrame(animate);
      pJSDom.canvas.ctx.clearRect(0, 0, pJSDom.canvas.w, pJSDom.canvas.h);
      for(var i = 0; i < particles.length; i++){
        particles[i].update();
      }
    }
  
    /* init */
    pJSDom.fn.particlesCreate();
    animate();
  
    /* resize */
    window.addEventListener('resize', function(){
      pJSDom.canvas.w = canvas_el.offsetWidth;
      pJSDom.canvas.h = canvas_el.offsetHeight;
    });
  
    /* return */
    return pJSDom;
  };