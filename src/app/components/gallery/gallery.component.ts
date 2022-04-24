import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, NavigationEnd } from '@angular/router';
import { images_data } from 'src/database';

@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.sass']
})
export class GalleryComponent implements OnInit {

  images_data = images_data
  current_route = 'newcomers'

  constructor(private router : Router, private route: ActivatedRoute) {
    router.events.subscribe((val)=>{
      if(val instanceof NavigationEnd){
        if (this.current_route != this.route.snapshot.url[0].path){
          this.current_route = this.route.snapshot.url[0].path
          
        }
        
        
      }
    })
   }
  

  ngOnInit(): void {
    console.log(this.route.snapshot.url[0].path)
    

    var card_heights : number[] = []

    window.onload = function () {
      let newHeight = 30
      let i = 0
      let lastIndex = 4
      let parallax_types = ['parallaxSlow', 'parallaxMedium', 'parallaxHigh']
      document.querySelectorAll<HTMLElement>(".imageCard").forEach(element => {
        

        let newHorizontalChange = Math.floor(Math.random() * 7)+4; 
        if (i%2 == 0){
          newHorizontalChange = 0-newHorizontalChange
        }    
        newHeight+=Math.floor(Math.random() * 30);
        element.setAttribute('style', `position:relative; top:${newHeight}px; right:${newHorizontalChange}vw`)
        card_heights.push(element.clientHeight)

        window.addEventListener('scroll',function(){
          var value = 0- window.scrollY;
          
          if (element.classList.contains('parallaxHigh')){
            let movingSpeed = value*0.14
            element.style.top = `${movingSpeed}px`
          }
          else if (element.classList.contains('parallaxMedium')){
            let movingSpeed = value*0.08
            element.style.top = `${movingSpeed}px`
          }
          else if (element.classList.contains('parallaxSlow')){
            let movingSpeed = value*0.04
            element.style.top = `${movingSpeed}px`
          }
        })
        let randomIndex = Math.floor(Math.random() * 3)
        while(randomIndex == lastIndex){
          randomIndex = Math.floor(Math.random() * 3)
        }
        lastIndex = randomIndex
        element.classList.add(parallax_types[randomIndex])
        i++
      });
    }
  }
  getRandomInt(max: number) {
    return Math.floor(Math.random() * max);
  }
}
