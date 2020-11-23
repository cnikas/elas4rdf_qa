import { Component, OnInit } from '@angular/core';
import { GetResponseService } from '../get-Response.service'
import { Response, Entity } from '../interfaces';
 
@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit {

  constructor(private getAnswerService: GetResponseService	) { }

  response: Response;
  showEntityModal: boolean;
  showTypeModal: boolean;
  checkedCategory: string;


  getResponse(): void {
    this.getAnswerService.getResponse()
        .subscribe(response => this.response = response);
  }

  ngOnInit() {
  	this.showEntityModal = false;
    this.showTypeModal = false;
    this.getResponse();
    this.checkedCategory = this.response.category;
  }

  isUri(s:string): boolean {
    return (s.startsWith('http://') ? true : false);
  }

  toggleTypeModal(): void {
    this.showTypeModal = !this.showTypeModal;
  }

  toggleEntityModal(): void {
    this.showEntityModal = !this.showEntityModal;
  }

  onCategoryChange(c: string): void {
    this.checkedCategory = c
  }

  deleteType(t: string): void {
    const index = this.response.types.indexOf(t);
    if (index > -1) {
      this.response.types.splice(index, 1);
    }
  }

  deleteEntity(e: Entity): void {
    const index = this.response.entities.indexOf(e);
    if (index > -1) {
      this.response.entities.splice(index, 1);
    }
  }

}
