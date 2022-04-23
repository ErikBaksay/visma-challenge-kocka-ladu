import { Component, OnInit } from '@angular/core';
import { images_data } from 'src/database';

@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.sass']
})
export class GalleryComponent implements OnInit {

  images_data = images_data
  parallax_types = ['parallaxSlow','parallaxMedium','parallaxHigh']

  constructor() { }

  ngOnInit(): void {
    const container = document.getElementById('container');
    console.log(container);
    
    for (let i = 0; i < container!.children.length; i++) {
      console.log(container!.children[i]);
  }

  }
    parallaxTypeGenerator(){
      return this.parallax_types[Math.floor(Math.random()*3)]
    }
}