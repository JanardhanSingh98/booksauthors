import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .responseid import response_id as rid


class BooksListApi(APIView):

    @staticmethod
    def get(request):
        # logging will help me to detect where exactly the error has occurred at backend side
        logging.info(msg='Inside book list get api [rid] : [{}]'.format(rid()))
        books = Book.objects.all()
        get_all_books = BookSerializers(books, many=True)
        return Response({'code': 1000, 'message': get_all_books.data, 'status': True, 'rid': rid()},
                        status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        logging.info(msg='Inside book list post api [rid] : [{}]'.format(rid()))
        book_serializer = BookSerializers(data=request.data)
        if book_serializer.is_valid():
            book_serializer.save()
            logging.info(msg='Book created with id : [{}]'.format(book_serializer.data['bo_id']))
            return Response({'code': 1000, 'message': 'Book created with id : \'{}\''.format(book_serializer.data['bo_id']),
                            'status': True, 'rid': rid()}, status=status.HTTP_200_OK)
        logging.error('Book serializer is not valid [rid] : [{}] \n{}'.format(rid(), book_serializer.errors))
        return Response({'code': 1001, 'message': book_serializer.errors, 'status': False, 'rid': rid()},
                        status=status.HTTP_400_BAD_REQUEST)


class BookDetailsApi(APIView):

    @staticmethod
    def get_object(uuid):
        logging.info(msg='fetching book object from database')
        try:
            return Book.objects.get(book_uuid=uuid)
        except Book.DoesNotExist:
            return Response('Book Not Found', status=status.HTTP_404_NOT_FOUND)

    # @staticmethod
    def get(self, request):
        logging.info(msg='Inside book details get api [rid] : [{}]'.format(rid()))
        if 'uuid' not in request.GET:
            logging.error(msg='user has not given uuid in not in request [rid] : [{}]'.format(rid()))
            return Response('uuid required in request', status=status.HTTP_400_BAD_REQUEST)
        uuid = request.GET['uuid']
        try:
            if uuid == '':
                logging.error(msg='user has not given uuid value in request [rid] : [{}]'.format(rid()))
                return Response('uuid value is required in request', status=status.HTTP_400_BAD_REQUEST)
            books = self.get_object(uuid)
            serializer = BookSerializers(books)
            au = Author.objects.values('author_uuid', 'first_name', 'last_name', 'email').get(id=serializer.data['au_id'])
            newdict = {}
            newdict.update(serializer.data)
            newdict.update(au)
            logging.info('successfully get the book [rid] : [{}] \n{}'.format(rid(), newdict))
            return Response({'code': 1000, 'message': newdict, 'status': True, 'rid': rid()},
                            status=status.HTTP_200_OK)
        except Exception as fail:
            logging.error(msg='Book with id - [{}] not found [rid] : [{}] failed : [{}]'.format(uuid, rid(), fail))
            return Response({'code': 1001, 'message': 'Book not found with id \'{}\''.format(uuid),
                             'status': False, 'rid': rid()}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        logging.info(msg='Inside book details put api [rid] : [{}]'.format(rid()))
        if 'uuid' not in request.GET:
            logging.error(msg='user has not given uuid in not in request [rid] : [{}]'.format(rid()))
            return Response('uuid req in req')
        uuid = request.GET['uuid']
        try:
            if uuid == '':
                logging.error(msg='user has not given uuid value in request [rid] : [{}]'.format(rid()))
                return Response('uuid is req')
            books = self.get_object(uuid)
            serializer = BookSerializers(books, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logging.info('successfully updated the book details [rid] : [{}] \n{}'.format(rid(), serializer.data))
                return Response({'code': 1000, 'message': 'book with id \'{}\' updated successfully'.format(uuid),
                                 'status': True, 'rid': rid()}, status=status.HTTP_200_OK)
            logging.error('failed updated the book details [rid] : [{}] \n{}'.format(rid(), serializer.errors))
            return Response({'code': 1002, 'message': serializer.errors,
                             'status': False, 'rid': rid()}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as fail:
            logging.error(msg='Book with id - [{}] not found [rid] : [{}] failed : [{}]'.format(uuid, rid(), fail))
            return Response({'code': 1001, 'message': 'Book not found with id \'{}\''.format(uuid),
                             'status': False, 'rid': rid()}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if 'uuid' not in request.GET:
            return Response('uuid req in req')
        uuid = request.GET['uuid']
        try:
            if uuid == '':
                logging.error(msg='user has not given uuid value in request [rid] : [{}]'.format(rid()))
                return Response('uuid is req')
            books = self.get_object(uuid)
            books.delete()
            logging.info(msg='successfully deleted the book with [uuid] : [{}] [rid] : [{}] '.format(uuid, rid()))
            return Response({'code': 1000, 'message': 'book with id \'{}\' deleted successfully'.format(uuid),
                             'status': True, 'rid': rid()}, status=status.HTTP_200_OK)
        except Exception as fail:
            logging.error(msg='Book with id - [{}] not found [rid] : [{}] failed : [{}]'.format(uuid, rid(), fail))
            return Response({'code': 1001, 'message': 'Book not found with id \'{}\''.format(uuid),
                             'status': False, 'rid': rid()}, status=status.HTTP_400_BAD_REQUEST)


class AuthorListApi(APIView):

    @staticmethod
    def get(request):
        logging.info(msg='inside author list api [rid] : [{}]'.format(rid()))
        author = Author.objects.all()
        get_all_author = AuthorSerializers(author, many=True)
        return Response({'code': 1000, 'message': get_all_author.data, 'status': True, 'rid': rid()},
                        status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        logging.info(msg='Inside author list post api [rid] : [{}]'.format(rid()))
        author_serializer = AuthorSerializers(data=request.data)
        if author_serializer.is_valid():
            author_serializer.save()
            logging.info(msg='author created with id : {}'.format(author_serializer.data))
            return Response({'code': 1000, 'message': 'author created with uuid [{}]'.format(author_serializer.data['au_id']),
                             'status': True, 'rid': rid()}, status=status.HTTP_200_OK)
        logging.error('author serializer is not valid [rid] : [{}] \n{}'.format(rid(), author_serializer.errors))
        return Response({'code': 1001, 'message': author_serializer.errors, 'status': False, 'rid': rid()},
                        status=status.HTTP_400_BAD_REQUEST)
