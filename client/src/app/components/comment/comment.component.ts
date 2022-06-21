import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Comment } from '../../services/comment/Comment';
import { CommentService } from '../../services/comment/comment.service';

@Component({
  selector: 'app-comment',
  templateUrl: './comment.component.html',
  styleUrls: ['./comment.component.scss']
})
export class CommentComponent implements OnInit {
  @Input() comment?: Comment;
  
  @Output() deleteCommentEvent = new EventEmitter()
  constructor(
    private commentService: CommentService
  ) { }

  ngOnInit(): void { 
  }
  
  deleteComment() {
    if (this.comment)
      this.commentService.deleteComment(this.comment.id).subscribe({complete: () => {
        this.deleteCommentEvent.emit()
      }})
  }
}
