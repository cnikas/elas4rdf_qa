import { TestBed } from '@angular/core/testing';

import { GetResponseService } from './get-response.service';

describe('GetResponseService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: GetResponseService = TestBed.get(GetResponseService);
    expect(service).toBeTruthy();
  });
});
