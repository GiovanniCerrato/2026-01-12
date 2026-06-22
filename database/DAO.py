from database.DB_connect import DBConnect
from model.Constructor import Constructor
from model.Edge import Edge


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(a1,a2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.constructorId , c.constructorRef , c.name , c.nationality 
                    from constructors c , results r , races ra
                    where c.constructorId = r.constructorId and r.raceId = ra.raceId 
                    and r.`position` is not null
                    and ra.year between %s and %s"""


        cursor.execute(query,(a1,a2))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(a1, a2, idMapC):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.constructorid as idC1 , t2.constructorid as idC2, count(distinct t1.driverid ) as weight
                    from (select c.constructorId, r.driverId, ra.raceId 
                    from constructors c , results r , races ra 
                    where c.constructorId = r.constructorId and r.raceId = ra.raceId 
                    and r.`position` is not null
                    and ra.year between %s and %s)as t1, 
                    (select c.constructorId , r.driverId , ra.raceId 
                    from constructors c , results r , races ra
                    where c.constructorId = r.constructorId and r.raceId = ra.raceId
                    and r.`position` is not null
                    and ra.year between %s and %s) as t2
                    where t1.driverId = t2.driverId and t1.raceId != t2.raceId and t1.constructorId != t2.constructorId and t1.constructorid<t2.constructorid 
                    group by t1.constructorid, t2.constructorid
                    order by t1.constructorid asc"""

        cursor.execute(query, (a1, a2,a1,a2))



        for row in cursor:
            c1 = idMapC[row["idC1"]]
            c2 = idMapC[row["idC2"]]
            results.append(Edge(c1,c2,row["weight"]))

        cursor.close()
        conn.close()
        return results

