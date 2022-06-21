import { Component, ElementRef, EventEmitter, OnInit, Output, ViewChild } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { BaseForm } from 'src/app/base-class/base-form';
import { AuthService } from 'src/app/services/auth/auth.service';
import { EventManagerService } from 'src/app/services/event-manager/event-manager.service';

@Component({
  selector: 'app-login-form',
  templateUrl: './login-form.component.html',
  styleUrls: ['./login-form.component.scss']
})
export class LoginFormComponent extends BaseForm implements OnInit {

  loginForm = this.formBuilder.group({
    login: '',
    password: ''
  });
  error = false

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    eventManagerService: EventManagerService,
  ) {
    super(eventManagerService)
  }

  ngOnInit(): void {
    this.error = false
  }
  
  onSubmit(): void {
    this.authService.login(
      this.loginForm.value.login,
      this.loginForm.value.password
    ).subscribe({ 
      next: () => {
        this.eventManagerService.userChangedEmit();
      },
      error: () => {
        this.error = true
      }
    })
  }
}
