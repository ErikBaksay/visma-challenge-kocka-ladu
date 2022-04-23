import { Component, OnInit } from '@angular/core';
import { images_data } from 'src/database';

@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.sass']
})
export class GalleryComponent implements OnInit {

  images_data = images_data
  parallax_types = ['parallaxSlow', 'parallaxMedium', 'parallaxHigh']

  constructor() { }

  ngOnInit(): void {
    var card_heights : number[] = []

    window.onload = function () {
      let newHeight = 30
      let i = 0
      document.querySelectorAll<HTMLElement>(".imageCard").forEach(element => {
        

        let newHorizontalChange = Math.floor(Math.random() * 7)+4; 
        if (i%2 == 0){
          newHorizontalChange = 0-newHorizontalChange
        }    
        newHeight+=Math.floor(Math.random() * 30);
        element.setAttribute('style', `position:relative; top:${newHeight}px; right:${newHorizontalChange}vw`)
        card_heights.push(element.clientHeight)

        window.addEventListener('scroll',function(){
          var value = window.scrollY;
          
          if (element.classList.contains('parallaxHigh')){
            let movingSpeed = value*0.2
            element.style.top = `${movingSpeed}px`
          }
          else if (element.classList.contains('parallaxMedium')){
            let movingSpeed = value*0.1
            element.style.top = `${movingSpeed}px`
          }
          else if (element.classList.contains('parallaxSlow')){
            let movingSpeed = value*0.05
            element.style.top = `${movingSpeed}px`
          }
        })

        i++
      });
    }

  }
  getRandomInt(max: number) {
    return Math.floor(Math.random() * max);
  }


}
