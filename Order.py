from collections import dequeue
class orders:
    def __init__(self):
        # FIFO queue of orders
        self.buy_orders = []
        self.sell_orders = []
        self.execution_id = 1 #IDs will start sequentially from 1

    def accept_order(self, order):
        executions = []
        if order.side == "Buy":
            while len(self.sell_orders) > 0:
                bestprice = self.sell_orders[0]
                if order.Price < bestprice.Price:
                    break # cannot match price to lowest sell price
                # remove the sell order if it matches the buy price
                self.sell_orders.pop(0)
                quantity = min(order.Quantity, bestprice.Quantity) # use the minimum of the quanities in buy and sell matched order
                execution = {
                    "Execution ID" : self.execution_id,
                    "Price": bestprice.Price,
                    "Quantity": quantity,
                    "Sell-OrderID": bestprice.orderID,
                    "Buy-OrderID": order.orderID
                }
                executions.append(execution)
                self.execution_id+=1
                #Still need to satisfy remaining quantity
                order.Quantity-=quantity 
                #update remaining quantity in sell order
                bestprice.Quantity-=quantity
                #if more left in sell order push to front since it was the best price and should be prioritised
                if bestprice.Quantity>0:
                    self.sell_orders.insert(0, bestprice)
                # break if order quantity is satisfied
                if order.quantity == 0:
                    break
            # if order unfulfilled, add in price time priority
            if order.Quantity > 0:
                position = 0 #position to insert buy order
                while position<len(self.buy_orders):
                    exisitingOrder = self.buy_orders[position]
                    if order.Price>exisitingOrder.Price:
                        #higher price is prioritised
                        break
                    #move past orders at the same price
                    position += 1
                self.buy_orders.insert(position, order)
        else:
            while len(self.buy_orders) > 0:
                #highest price in buy orders is at position 0
                bestprice2 = self.buy_orders[0]
                if bestprice2.Price < order.Price:
                    break
                #remove matched order
                self.buy_orders.pop(0)
                quantity = min(bestprice2.Price, order.Price)
                execution = {
                    "Execution ID" : self.execution_id,
                    "Price": bestprice2.Price,
                    "Quantity": quantity,
                    "Sell-OrderID": order.orderID,
                    "Buy-OrderID": bestprice2.orderID
                }
                executions.append(execution)



