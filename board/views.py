from rest_framework import generics
from .models import Board, Comment
from .serializers import BoardSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from django.shortcuts import get_object_or_404

class BoardListCreateView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    
class BoardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    
#조회수
class IncrementViews(APIView):
    def put(self, request, pk):
        try:
            # 게시글 가져오기
            board = Board.objects.get(pk=pk)
            
            # 조회수 증가
            board.views_count += 1
            board.save()
            
            # 증가된 조회수와 함께 게시글 정보 반환
            return Response({'views_count': board.views_count}, status=status.HTTP_200_OK)
        
        except Board.DoesNotExist:
            return Response({'message': 'Board not found'}, status=status.HTTP_404_NOT_FOUND)
        
# 댓글 조회/작성
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        board_id = self.kwargs['pk']
        return Comment.objects.filter(board_id=board_id)
    
# 댓글 수정/삭제
class CommentUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        board_id = self.kwargs['pk']
        comment_id = self.kwargs['comment_id']
        return Comment.objects.filter(board_id=board_id, id=comment_id)
    
    def get_object(self):
        board_id = self.kwargs['pk']
        comment_id = self.kwargs['comment_id']
        return get_object_or_404(Comment, board_id=board_id, id=comment_id)