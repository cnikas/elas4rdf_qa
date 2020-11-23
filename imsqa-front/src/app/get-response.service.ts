import { Injectable } from '@angular/core';


import { Observable, of } from 'rxjs';
import { Response } from './interfaces';
import { RESPONSE } from './mock-response';

@Injectable({
  providedIn: 'root'
})

export class GetResponseService {
  

  constructor() { }

  getResponse(): Observable<Response> {
    return of(RESPONSE);
  }
}
